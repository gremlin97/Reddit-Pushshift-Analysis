# Import required libraries
# Do not install/import any additional libraries
import psycopg2
import psycopg2.extras
import json
import csv
import math 


# Lets define some of the essentials
# We'll define these as global variables to keep it simple
username = "postgres"
password = "postgres"
dbname = "assignment3"
host = "127.0.0.1"


def get_open_connection():
    """
    Connect to the database and return connection object
    
    Returns:
        connection: The database connection object.
    """

    return psycopg2.connect(f"dbname='{dbname}' user='{username}' host='{host}' password='{password}'")




def load_data(table_name, csv_path, connection, header_file):
    """
    Create a table with the given name and load data from the CSV file located at the given path.

    Args:
        table_name (str): The name of the table where data is to be loaded.
        csv_path (str): The path to the CSV file containing the data to be loaded.
        connection: The database connection object.
        header_file (str): The path to where the header file is located
    """

    cursor = connection.cursor()

    # Creating the table
    with open(header_file) as json_data:
        header_dict = json.load(json_data)

    table_rows_formatted = (", ".join(f"{header} {header_type}" for header, header_type in header_dict.items()))
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {table_rows_formatted}
            )'''

    cursor.execute(create_table_query)
    connection.commit()


    # # TODO: Implement code to insert data here
    with open(csv_path, 'r') as File:
        # Using the copy_expert method with the CSV data and table name
        cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", file=File)
    connection.commit()
    cursor.close()


def range_partition(data_table_name, partition_table_name, num_partitions, header_file, column_to_partition, connection):
    """
    Use this function to partition the data in the given table using a range partitioning approach.

    Args:
        data_table_name (str): The name of the table that contains the data loaded during load_data phase.
        partition_table_name (str): The name of the table to be created for partitioning.
        num_partitions (int): The number of partitions to create.
        header_file (str): path to the header file that contains column headers and their data types
        column_to_partition (str): The column based on which we are creating the partition.
        connection: The database connection object.
    """

    # TODO: Implement code to perform range_partition here
    
    with open(header_file) as File:
        header = json.load(File)
    column_types = ', '.join(f"{col} {header[col]}" for col in header)
    column_to_partition_type = header[column_to_partition]

    cursor = connection.cursor()
    cursor.execute(f"SELECT MIN({column_to_partition}), MAX({column_to_partition}) FROM {data_table_name}")
    min_value, max_value = cursor.fetchone()

    step = math.ceil(((max_value - min_value)+1) / num_partitions)
    boundaries = [(min_value + i * step) for i in range(num_partitions+1)]  

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {partition_table_name} ({column_types}) PARTITION BY RANGE ({column_to_partition})")
    
    for i in range(num_partitions):
        cursor.execute(f"CREATE TABLE {partition_table_name}{i} PARTITION OF {partition_table_name} FOR VALUES FROM ({boundaries[i]}) TO ({boundaries[i+1]})")
    
    cursor.execute(f'INSERT INTO {partition_table_name} SELECT * FROM {data_table_name}')
    
    connection.commit()
    cursor.close()



def round_robin_partition(data_table_name, partition_table_name, num_partitions, header_file, connection):
    """
    Use this function to partition the data in the given table using a round-robin approach.

    Args:
        data_table_name (str): The name of the table that contains the data loaded during load_data phase.
        partition_table_name (str): The name of the table to be created for partitioning.
        num_partitions (int): The number of partitions to create.
        header_file (str): path to the header file that contains column headers and their data types
        connection: The database connection object.
    """

    # TODO: Implement code to perform round_robin_partition here
    
    cursor = connection.cursor()

    # Creating the table
    with open(header_file) as json_data:
        header_dict = json.load(json_data)

    table_rows_formatted = (", ".join(f"{header} {header_type}" for header, header_type in header_dict.items()))
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {partition_table_name} (
            {table_rows_formatted}
            )'''

    cursor.execute(create_table_query)
    connection.commit()
    
    attribute_list = list(header_dict.keys())
    columns = ','.join(attribute_list)
    
    for i in range(num_partitions):
        table_name = f"{partition_table_name}{i}"
        cursor.execute(f"CREATE TABLE {table_name} () INHERITS ({partition_table_name}); INSERT INTO {table_name} SELECT {columns} FROM (SELECT *, ROW_NUMBER() OVER () FROM {data_table_name}) t WHERE MOD(ROW_NUMBER - 1, {num_partitions}) = {i}")
    
    roundrobinTrigger = f'''
        CREATE OR REPLACE FUNCTION roundrobin()
        RETURNS TRIGGER AS $$
        DECLARE
            partname TEXT := '{partition_table_name}';
            partcnt INTEGER;
        BEGIN
            SELECT MOD((SELECT COUNT(*) FROM {partition_table_name}), {num_partitions}) INTO partcnt;
            partname := partname || CAST(partcnt as TEXT);
            IF (TG_OP = 'INSERT') THEN 
                EXECUTE CONCAT('INSERT INTO ', quote_ident(partname), ' VALUES ($1.*)') USING NEW;
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
    '''

    cursor.execute(roundrobinTrigger)

    cursor.execute(f'CREATE TRIGGER round_robin_insert BEFORE INSERT ON {partition_table_name} FOR EACH ROW EXECUTE FUNCTION roundrobin()')

    connection.commit()
    cursor.close()
    



def delete_partitions(table_name, num_partitions, connection):
    """
    This function in NOT graded and for your own testing convinience.
    Use this function to delete all the partitions that are created by you.

    Args:
        table_name (str): The name of the table containing the partitions to be deleted.
        num_partitions (int): The number of partitions to be deleted.
        connection: The database connection object.
    """

    # TODO: UNGRADED: Implement code to delete partitions here
    raise Exception("Function yet to be implemented!")


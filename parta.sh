#!/bin/sh

start=$(date +%s)
psql postgresql://postgres:postgres@localhost/postgres < copy.sql
PGPASSWORD=postgres pg_bulkload -i ./authors.csv -O author -U postgres -d postgres -h 127.0.0.1 -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -o "WRITER=PARALLEL"
PGPASSWORD=postgres pg_bulkload -i ./subreddits.csv -O subreddit -U postgres -d postgres -h 127.0.0.1 -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -o "WRITER=PARALLEL"
PGPASSWORD=postgres pg_bulkload -i ./submissions.csv -O submissions -U postgres -d postgres -h 127.0.0.1 -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -o "WRITER=PARALLEL"
PGPASSWORD=postgres pg_bulkload -i ./comments.csv -O comments -U postgres -d postgres -h 127.0.0.1 -o "TYPE=CSV" -o "DELIMITER=," -o "SKIP=1" -o "WRITER=PARALLEL"
end=$(date +%s)
echo "Time taken to copy to database is: $(($end-$start)) seconds"
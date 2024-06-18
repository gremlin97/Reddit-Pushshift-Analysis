CREATE TABLE IF NOT EXISTS author(
    id text, 
    retrieved_on integer,
    name text PRIMARY KEY,
    created_utc integer,
    link_karma integer,
    comment_karma integer,
    profile_img text,
    profile_color text,
    profile_over_18 boolean
);

CREATE TABLE IF NOT EXISTS subreddit(
    banner_background_image text,
    created_utc integer,
    description text,
    display_name text,
    header_img text,
    hide_ads boolean,
    id text,
    over_18 boolean,
    public_description text,
    retrieved_utc integer,
    name text PRIMARY KEY,
    subreddit_type text,
    subscribers integer,
    title text,
    whitelist_status text
);

ALTER TABLE IF EXISTS subreddit ADD CONSTRAINT unique_CompKey UNIQUE(name, display_name);

CREATE TABLE IF NOT EXISTS submissions(
    downs integer,
    url text,
    id text PRIMARY KEY,
    edited boolean,
    num_reports integer,
    created_utc integer,
    name text,
    title text,
    author text,
    permalink text,
    num_comments integer,
    likes boolean,
    subreddit_id text,
    ups integer
);

ALTER TABLE IF EXISTS submissions ADD CONSTRAINT submissionsAuthorFK FOREIGN KEY(author) REFERENCES author(name);

ALTER TABLE IF EXISTS submissions ADD CONSTRAINT submissionsSubredditIdFK FOREIGN KEY(subreddit_id) REFERENCES subreddit(name);

CREATE TABLE IF NOT EXISTS comments(
    distinguished text,
    downs integer,
    created_utc integer,
    controversiality integer,
    edited boolean,
    gilded integer,
    author_flair_css_class text,
    id text PRIMARY KEY,
    author text,
    retrieved_on integer,
    score_hidden boolean,
    subreddit_id text,
    score integer,
    name text,
    author_flair_text text,
    link_id text,
    archived boolean,
    ups integer,
    parent_id text,
    subreddit text,
    body text
);

ALTER TABLE IF EXISTS comments ADD CONSTRAINT commentsAuthorFK FOREIGN KEY(author) REFERENCES author(name);

ALTER TABLE IF EXISTS comments ADD CONSTRAINT commentsSubredditFK FOREIGN KEY(subreddit, subreddit_id) REFERENCES subreddit(display_name, name);
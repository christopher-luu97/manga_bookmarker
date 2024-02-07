-- This script is to be ran after create_manga_tables.sql has been executed due to referencing

CREATE TABLE user_table (
    -- This table holds the user details
    userid UUID PRIMARY KEY,
    username VARCHAR(100),
    password_hash VARCHAR(255),
    user_email VARCHAR(255),
    create_date TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE user_genre_preferences (
    -- This table holds the genres that a user is interested in
    user_genre_preference_id UUID PRIMARY KEY,
    userid UUID REFERENCES user_table(userid),
    genre VARCHAR(100),
    preference_score INTEGER,
    last_updated TIMESTAMP
);

CREATE TABLE user_reading_history (
    -- Gather the reading history of a user
    reading_history_id UUID PRIMARY KEY,
    userid UUID REFERENCES user_table(userid),
    manga_chapter_url_id UUID REFERENCES manga_chapter_url_store(manga_chapter_url_id),
    reading_date DATE,
    pages_read INTEGER
);

CREATE TABLE user_manga_follows (
    user_manga_follow_id UUID PRIMARY KEY,
    userid UUID REFERENCES user_table(userid),
    manga_id UUID REFERENCES manga_table(manga_id),
    date_followed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



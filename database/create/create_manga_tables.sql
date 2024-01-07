CREATE TABLE website_table (
    -- This table contains the key websites that are supported
    website_id UUID PRIMARY KEY,
    website_url VARCHAR(255),
    website_status VARCHAR(100),
    date_checked TIMESTAMP
);

CREATE TABLE manga_table (
    -- Table that maps a manga name to an ID, e.g. 1, One Piece
    manga_id UUID PRIMARY KEY,
    manga_name VARCHAR(255)
);

CREATE TABLE manga_path_table (
    -- Maps a manga path to a manga name and website
    -- Example manga path is /mangas/5/one-piece
    -- when concat with website, we get example.com/mangas/5/one-piece
    manga_path_id UUID PRIMARY KEY,
    manga_id UUID REFERENCES manga_table(manga_id),
    website_id UUID REFERENCES website_table(website_id),
    manga_path VARCHAR(255)
);

CREATE TABLE manga_genre_table (
    -- This table holds the genre for each manga
    manga_genre_id UUID PRIMARY KEY,
    manga_id UUID REFERENCES manga_table(manga_id),
    genre VARCHAR(100)
);

CREATE TABLE manga_name_mappings (
    -- This table is used to map any manga that has different names
    -- Example is "Battle through the Heavens" which is also "Doupou Canqiong"
    manga_name_mapping_id UUID PRIMARY KEY,
    website_id UUID REFERENCES website_table(website_id),
    manga_id UUID REFERENCES manga_table(manga_id),
    manga_name VARCHAR(255)
);

CREATE TABLE manga_chapter_url_store (
    -- This is the table that stores the latest chapter URL
    -- This table is updated daily and is read into the frontend
    -- This table displays latest chapter informatoion and direct links to them
    manga_chapter_url_id UUID PRIMARY KEY,
    manga_id UUID REFERENCES manga_table(manga_id),
    website_id UUID REFERENCES website_table(website_id),
    manga_path_id UUID REFERENCES manga_path_table(manga_path_id),
    chapter_url VARCHAR(255),
    number_of_pages INTEGER,
    chapter_url_status VARCHAR(100),
    chapter_number INT,
    date_checked TIMESTAMP
);

CREATE TABLE manga_thumbnail (
    -- This table stores the thumbnail of the manga that has been scraped
    -- Ideally should not be stored in RDBMS but in cloud
    manga_thumbnail_id UUID PRIMARY KEY,
    manga_id UUID REFERENCES manga_table(manga_id),
    website_id UUID REFERENCES website_table(website_id),
    manga_path_id UUID REFERENCES manga_path_table(manga_path_id),
    thumbnail_url VARCHAR(255)
);
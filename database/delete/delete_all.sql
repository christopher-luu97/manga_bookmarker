-- Test script for deleting all records in database

-- Start by deleting records from tables with foreign key dependencies
DELETE FROM manga_thumbnail;
DELETE FROM manga_chapter_url_store;
DELETE FROM manga_name_mappings;
DELETE FROM manga_genre_table;
DELETE FROM manga_path_table;

DELETE FROM manga_table;
DELETE FROM website_table;

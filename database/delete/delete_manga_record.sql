CREATE OR REPLACE PROCEDURE delete_manga_record(user_id UUID, manga_id UUID)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Delete related thumbnails
    DELETE FROM manga_thumbnail WHERE manga_id IN (SELECT manga_id FROM manga_table WHERE manga_id = manga_id AND userid = user_id);

    -- Delete related chapter URLs
    DELETE FROM manga_chapter_url_store WHERE manga_id IN (SELECT manga_id FROM manga_table WHERE manga_id = manga_id AND userid = user_id);

    -- Delete related name mappings
    DELETE FROM manga_name_mappings WHERE manga_id IN (SELECT manga_id FROM manga_table WHERE manga_id = manga_id AND userid = user_id);

    -- Delete related genres
    DELETE FROM manga_genre_table WHERE manga_id IN (SELECT manga_id FROM manga_table WHERE manga_id = manga_id AND userid = user_id);

    -- Delete related paths
    DELETE FROM manga_path_table WHERE manga_id IN (SELECT manga_id FROM manga_table WHERE manga_id = manga_id AND userid = user_id);

    -- Finally, delete the manga record itself
    DELETE FROM manga_table WHERE manga_id = manga_id AND userid = user_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_manga_record(p_manga_id UUID)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Deleting from child tables first
    DELETE FROM manga_chapter_url_store WHERE manga_id = p_manga_id;
    DELETE FROM manga_genre_table WHERE manga_id = p_manga_id;
    DELETE FROM manga_name_mappings WHERE manga_id = p_manga_id;
    DELETE FROM manga_thumbnail WHERE manga_id = p_manga_id;
    DELETE FROM manga_path_table WHERE manga_id = p_manga_id;

    -- Finally, delete from the manga_table
    DELETE FROM manga_table WHERE manga_id = p_manga_id;
END;
$$;

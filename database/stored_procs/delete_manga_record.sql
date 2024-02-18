CREATE OR REPLACE PROCEDURE delete_manga_record(input_userid UUID, p_manga_id UUID)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Check if the manga belongs to the user before deletion
    IF (SELECT COUNT(*) FROM manga_table WHERE manga_id = p_manga_id AND userid = input_userid) > 0 THEN
        -- Deleting from child tables first
        DELETE FROM manga_chapter_url_store WHERE manga_id = p_manga_id;
        DELETE FROM manga_genre_table WHERE manga_id = p_manga_id;
        DELETE FROM manga_name_mappings WHERE manga_id = p_manga_id;
        DELETE FROM manga_thumbnail WHERE manga_id = p_manga_id;
        DELETE FROM manga_path_table WHERE manga_id = p_manga_id;

        -- Finally, delete from the manga_table
        DELETE FROM manga_table WHERE manga_id = p_manga_id;
    ELSE
        RAISE EXCEPTION 'Manga does not belong to the user.';
    END IF;
END;
$$;

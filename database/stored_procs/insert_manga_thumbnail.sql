CREATE OR REPLACE PROCEDURE insert_manga_thumbnail(
    p_userid UUID,
    p_manga_thumbnail_id UUID,
    p_manga_id UUID,
    p_website_id UUID,
    p_manga_path_id UUID,
    p_thumbnail_url VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verify that the manga_id belongs to the user before inserting the thumbnail
    IF NOT EXISTS (
        SELECT 1 FROM manga_table
        WHERE manga_id = p_manga_id AND userid = p_userid
    ) THEN
        RAISE EXCEPTION 'User does not own the specified manga, cannot insert thumbnail.';
    END IF;

    -- Proceed to insert the thumbnail after confirming ownership
    INSERT INTO manga_thumbnail (
        manga_thumbnail_id,
        manga_id,
        website_id,
        manga_path_id,
        thumbnail_url
    ) VALUES (
        p_manga_thumbnail_id,
        p_manga_id,
        p_website_id,
        p_manga_path_id,
        p_thumbnail_url
    );
END;
$$;

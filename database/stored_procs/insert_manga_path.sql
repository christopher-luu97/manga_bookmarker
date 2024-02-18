CREATE OR REPLACE PROCEDURE insert_manga_path(
    p_userid UUID,
    p_manga_path_id UUID,
    p_manga_id UUID,
    p_website_id UUID,
    p_manga_path VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verify that the manga_id belongs to the user before inserting the manga path
    IF NOT EXISTS (
        SELECT 1 FROM manga_table
        WHERE manga_id = p_manga_id AND userid = p_userid
    ) THEN
        RAISE EXCEPTION 'User does not own the specified manga, cannot insert manga path.';
    END IF;

    -- Proceed to insert the manga path after confirming ownership
    INSERT INTO manga_path_table (
        manga_path_id,
        manga_id,
        website_id,
        manga_path
    ) VALUES (
        p_manga_path_id,
        p_manga_id,
        p_website_id,
        p_manga_path
    );
END;
$$;

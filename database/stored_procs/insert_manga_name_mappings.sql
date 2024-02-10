CREATE OR REPLACE PROCEDURE insert_manga_name_mapping(
    p_userid UUID,
    p_manga_name_mapping_id UUID,
    p_website_id UUID,
    p_manga_id UUID,
    p_manga_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Check if the manga_id belongs to the user before proceeding with the insert
    IF NOT EXISTS (
        SELECT 1 FROM manga_table
        WHERE manga_id = p_manga_id AND userid = p_userid
    ) THEN
        RAISE EXCEPTION 'User does not own the specified manga, cannot insert name mapping.';
    END IF;

    -- Proceed to insert the manga name mapping after ownership verification
    INSERT INTO manga_name_mappings (
        manga_name_mapping_id,
        website_id,
        manga_id,
        manga_name
    ) VALUES (
        p_manga_name_mapping_id,
        p_website_id,
        p_manga_id,
        p_manga_name
    );
END;
$$;

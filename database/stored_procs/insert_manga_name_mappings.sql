CREATE OR REPLACE PROCEDURE insert_manga_name_mapping(
    p_manga_name_mapping_id UUID,
    p_website_id UUID,
    p_manga_id UUID,
    p_manga_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
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

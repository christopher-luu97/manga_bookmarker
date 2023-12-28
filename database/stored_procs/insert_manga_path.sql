CREATE OR REPLACE PROCEDURE insert_manga_path(
    p_manga_path_id UUID,
    p_manga_id UUID,
    p_website_id UUID,
    p_manga_path VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
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

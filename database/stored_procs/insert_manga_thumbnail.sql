CREATE OR REPLACE PROCEDURE insert_manga_thumbnail(
    p_manga_thumbnail_id UUID,
    p_manga_id UUID,
    p_website_id UUID,
    p_manga_path_id UUID,
    p_thumbnail_url VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
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

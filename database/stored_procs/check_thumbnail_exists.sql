CREATE OR REPLACE FUNCTION check_thumbnail_exists(
    input_manga_id UUID,
    input_website_id UUID,
    input_manga_path_id UUID,
    input_thumbnail_url TEXT
) RETURNS BOOLEAN AS $$
BEGIN
    RETURN (SELECT COUNT(*) > 0 
            FROM manga_thumbnail
            WHERE manga_id = input_manga_id 
            AND website_id = input_website_id 
            AND manga_path_id = input_manga_path_id 
            AND thumbnail_url = input_thumbnail_url);
END;
$$ LANGUAGE plpgsql;

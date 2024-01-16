CREATE OR REPLACE FUNCTION check_chapter_url_exists(
    input_manga_id UUID,
    input_website_id UUID,
    input_manga_path_id UUID,
    input_chapter_url TEXT
) RETURNS BOOLEAN AS $$
BEGIN
    RETURN (SELECT COUNT(*) > 0 
            FROM manga_chapter_url_store
            WHERE manga_id = input_manga_id 
            AND website_id = input_website_id 
            AND manga_path_id = input_manga_path_id 
            AND chapter_url = input_chapter_url);
END;
$$ LANGUAGE plpgsql;

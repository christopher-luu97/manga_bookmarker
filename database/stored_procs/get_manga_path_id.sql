CREATE OR REPLACE FUNCTION get_manga_path_id(
    input_manga_id UUID,
    input_website_id UUID,
    input_manga_path TEXT
) RETURNS UUID AS $$
BEGIN
    RETURN (SELECT manga_path_id 
            FROM manga_path_table
            WHERE manga_id = input_manga_id 
            AND website_id = input_website_id 
            AND manga_path = input_manga_path);
END;
$$ LANGUAGE plpgsql;

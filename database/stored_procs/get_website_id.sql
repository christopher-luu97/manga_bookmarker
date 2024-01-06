CREATE OR REPLACE FUNCTION get_website_id_by_url(p_website_url VARCHAR)
RETURNS UUID AS $$
DECLARE
    result UUID;
BEGIN
    SELECT website_id INTO result FROM website_table WHERE website_url = p_website_url LIMIT 1;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

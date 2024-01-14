CREATE OR REPLACE FUNCTION get_manga_bookmarks()
RETURNS TABLE(
    manga_id UUID,
    manga_name VARCHAR,
    full_url VARCHAR,
    date_checked TIMESTAMP,
    website_status VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.manga_id,
        m.manga_name,
        w.website_url || p.manga_path AS full_url,
        w.date_checked,
        w.website_status
    FROM 
        manga_table m
        JOIN manga_path_table p ON m.manga_id = p.manga_id
        JOIN website_table w ON p.website_id = w.website_id;
END;
$$ LANGUAGE plpgsql;

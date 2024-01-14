CREATE OR REPLACE FUNCTION get_supported_websites()
RETURNS TABLE(
    website_id UUID,
    website_name VARCHAR,
    website_url VARCHAR,
    website_status VARCHAR,
    date_checked TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        w.website_id, 
        w.website_name,
        w.website_url,
        w.website_status,
        w.date_checked
    FROM 
        website_table w; 
END;
$$ LANGUAGE plpgsql;

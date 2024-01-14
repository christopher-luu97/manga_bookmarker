CREATE OR REPLACE FUNCTION get_website_paths()
RETURNS TABLE(
    manga_path_id UUID,
    manga_id UUID,
    manga_name VARCHAR,
    full_path VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        mp.manga_path_id,
        mp.manga_id,
        mt.manga_name,
        wt.website_url || mp.manga_path AS full_path
    FROM 
        manga_path_table mp
        INNER JOIN website_table wt ON mp.website_id = wt.website_id
        INNER JOIN manga_table mt ON mp.manga_id = mt.manga_id;
END;
$$ LANGUAGE plpgsql;

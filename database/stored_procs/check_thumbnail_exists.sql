CREATE OR REPLACE FUNCTION check_thumbnail_exists(
    input_userid UUID,
    input_manga_id UUID,
    input_website_id UUID,
    input_manga_path_id UUID,
    input_thumbnail_url TEXT
) RETURNS BOOLEAN AS $$
BEGIN
    RETURN (SELECT COUNT(*) > 0 
            FROM manga_thumbnail
            JOIN manga_table ON manga_table.manga_id = manga_thumbnail.manga_id
            WHERE manga_table.userid = input_userid
            AND manga_thumbnail.manga_id = input_manga_id 
            AND manga_thumbnail.website_id = input_website_id 
            AND manga_thumbnail.manga_path_id = input_manga_path_id 
            AND manga_thumbnail.thumbnail_url = input_thumbnail_url);
END;
$$ LANGUAGE plpgsql;

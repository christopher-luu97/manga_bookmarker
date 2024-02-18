CREATE OR REPLACE FUNCTION get_manga_data(input_userid UUID)
RETURNS TABLE(
    id UUID,
    title VARCHAR,
    chapter VARCHAR,
    lastUpdated TIMESTAMP,
    imageUrl VARCHAR,
    status VARCHAR,
    chapter_number INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.manga_id AS id,
        m.manga_name AS title,
        mc.chapter_url AS chapterLink,
        mc.date_checked AS lastUpdated,
        mt.thumbnail_url AS imageUrl,
        mc.chapter_url_status AS status,
        mc.chapter_number as chapter_number
    FROM 
        manga_table m
        JOIN manga_chapter_url_store mc ON m.manga_id = mc.manga_id
        LEFT JOIN manga_thumbnail mt ON m.manga_id = mt.manga_id
    WHERE m.userid = input_userid;
END;
$$ LANGUAGE plpgsql;

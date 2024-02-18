CREATE OR REPLACE FUNCTION check_chapter_url_exists(
    input_userid UUID,
    input_manga_id UUID,
    input_website_id UUID,
    input_manga_path_id UUID,
    input_chapter_url TEXT
) RETURNS BOOLEAN AS $$
BEGIN
    RETURN (SELECT COUNT(*) > 0 
            FROM manga_chapter_url_store
            JOIN manga_table ON manga_table.manga_id = manga_chapter_url_store.manga_id
            WHERE manga_table.userid = input_userid
            AND manga_chapter_url_store.manga_id = input_manga_id 
            AND manga_chapter_url_store.website_id = input_website_id 
            AND manga_chapter_url_store.manga_path_id = input_manga_path_id 
            AND manga_chapter_url_store.chapter_url = input_chapter_url);
END;
$$ LANGUAGE plpgsql;

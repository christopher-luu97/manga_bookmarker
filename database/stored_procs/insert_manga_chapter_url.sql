CREATE OR REPLACE PROCEDURE insert_manga_chapter_url_store(
    p_manga_chapter_url_id UUID,
    p_manga_id UUID,
    p_website_id UUID,
    p_manga_path_id UUID,
    p_chapter_url VARCHAR,
    p_number_of_pages INTEGER,
    p_chapter_url_status VARCHAR,
    p_date_checked TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO manga_chapter_url_store (
        manga_chapter_url_id,
        manga_id,
        website_id,
        manga_path_id,
        chapter_url,
        number_of_pages,
        chapter_url_status,
        date_checked
    ) VALUES (
        p_manga_chapter_url_id,
        p_manga_id,
        p_website_id,
        p_manga_path_id,
        p_chapter_url,
        p_number_of_pages,
        p_chapter_url_status,
        p_date_checked
    );
END;
$$;

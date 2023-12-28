CREATE OR REPLACE PROCEDURE insert_manga_genre(
    p_manga_genre_id UUID,
    p_manga_id UUID,
    p_genre VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO manga_genre_table (
        manga_genre_id,
        manga_id,
        genre
    ) VALUES (
        p_manga_genre_id,
        p_manga_id,
        p_genre
    );
END;
$$;

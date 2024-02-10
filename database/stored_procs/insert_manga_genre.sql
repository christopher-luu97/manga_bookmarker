CREATE OR REPLACE PROCEDURE insert_manga_genre(
    p_userid UUID,
    p_manga_genre_id UUID,
    p_manga_id UUID,
    p_genre VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Check if the manga_id belongs to the user
    IF NOT EXISTS (
        SELECT 1 FROM manga_table
        WHERE manga_id = p_manga_id AND userid = p_userid
    ) THEN
        RAISE EXCEPTION 'User does not own the specified manga, cannot insert genre.';
    END IF;

    -- Proceed to insert genre after ownership verification
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

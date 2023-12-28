CREATE OR REPLACE PROCEDURE insert_manga(
    p_manga_id UUID,
    p_manga_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO manga_table (
        manga_id,
        manga_name
    ) VALUES (
        p_manga_id,
        p_manga_name
    );
END;
$$;

CREATE OR REPLACE PROCEDURE insert_manga(
    p_userid UUID,
    p_manga_id UUID,
    p_manga_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Insert a new manga record, linking it to the user by their userid
    INSERT INTO manga_table (
        manga_id,
        userid,  -- Ensure this column is correctly referenced as per your table definition
        manga_name
    ) VALUES (
        p_manga_id,
        p_userid,  -- Link the manga to the user
        p_manga_name
    );
END;
$$;

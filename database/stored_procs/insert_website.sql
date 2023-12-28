CREATE OR REPLACE PROCEDURE insert_website(
    p_website_id UUID,
    p_website_url VARCHAR,
    p_website_status VARCHAR,
    p_date_checked TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO website_table (
        website_id,
        website_url,
        website_status,
        date_checked
    ) VALUES (
        p_website_id,
        p_website_url,
        p_website_status,
        p_date_checked
    );
END;
$$;

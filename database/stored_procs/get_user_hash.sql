CREATE OR REPLACE FUNCTION get_user_hash(_username VARCHAR(100))
RETURNS TABLE(password_hash VARCHAR(255)) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT password_hash FROM user_table WHERE username = _username;
END;
$$;

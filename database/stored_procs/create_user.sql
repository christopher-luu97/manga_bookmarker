CREATE OR REPLACE PROCEDURE createUser(
    _userid UUID,
    _username VARCHAR(100),
    _password_hash VARCHAR(255),
    _user_email VARCHAR(255),
    _create_date TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO user_table (userid, username, password_hash, user_email, create_date)
    VALUES (_userid, _username, _password_hash, _user_email, _create_date);
END;
$$;

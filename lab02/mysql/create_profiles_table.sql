CREATE TABLE profiles (
    user_id VARCHAR(100) NOT NULL, 
    user_name VARCHAR(100) NOT NULL, 
    user_address VARCHAR(100),
    user_mobile VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
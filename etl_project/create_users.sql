
CREATE TABLE users (
    _id SERIAL PRIMARY KEY,
    id VARCHAR,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    location_city VARCHAR(50) NOT NULL,
    location_country VARCHAR(50) NOT NULL,
    location_state  VARCHAR(50) NOT NULL,
    location_latitude FLOAT NOT NULL,
    location_longitude FLOAT NOT NULL,
    location_postcode VARCHAR(20),
    location_street_info VARCHAR(80),
    email VARCHAR(200) NOT NULL,
    gender VARCHAR(1) NOT NULL,
    login_username VARCHAR(100) NOT NULL,
    login_password VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    cell VARCHAR(15) NOT NULL,
    date_of_birth TIMESTAMP NOT NULL,
    age INTEGER NOT NULL,
    date_of_registration TIMESTAMP NOT NULL,
    photo_link VARCHAR(300) NOT NULL,
    extract_time TIMESTAMP NOT NULL,

    year_of_registration INTEGER NOT NULL,
    month_of_registration INTEGER NOT NULL,
    day_of_registration INTEGER NOT NULL,

    password_length INTEGER,
    loging_length INTEGER,
    transform_timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
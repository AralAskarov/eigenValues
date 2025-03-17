CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    number_of_sub_genres INTEGER NOT NULL DEFAULT 0,
    url TEXT
);
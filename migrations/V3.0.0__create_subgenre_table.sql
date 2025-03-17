CREATE TABLE sub_genres (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    main_genre VARCHAR(255) NOT NULL,
    no_of_books NUMERIC,
    url TEXT,
    -- CONSTRAINT fk_main_genre FOREIGN KEY (main_genre) REFERENCES genres(title)
);
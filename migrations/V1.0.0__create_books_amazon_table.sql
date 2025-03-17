CREATE TABLE IF NOT EXISTS books_amazon (
    unnamed_0 INTEGER,
    title VARCHAR(255),
    author VARCHAR(150),
    main_genre VARCHAR(100),
    sub_genre VARCHAR(100),
    type VARCHAR(50),
    price DECIMAL(10, 2),
    rating DECIMAL(3, 1),
    people_rated INTEGER,
    url TEXT
);
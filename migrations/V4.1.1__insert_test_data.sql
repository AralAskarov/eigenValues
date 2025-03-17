-- Тестовые пользователи
INSERT INTO users (username, password, age) VALUES
    ('john_doe', 'hashed_password_123', 28),
    ('alice_smith', 'hashed_password_456', 34),
    ('bob_johnson', 'hashed_password_789', 22);

-- Тестовые записи в таблице user_favorite_books
INSERT INTO user_favorite_books (user_id, book_title) VALUES
    (1, 'The Kite Runner'),
    (1, 'Black Holes (L) : The Reith Lectures'),
    (2, 'The Complete Novel of Sherlock Holmes'),
    (2, 'The Science of Storytelling'),
    (3, 'Lonely Planet India 19');

-- Тестовые предпочтения пользователей
INSERT INTO user_preferences (user_id, category, value, weight, count) VALUES
    -- Пользователь 1
    (1, 'Main Genre', 'Arts, Film & Photography', 3.8, 5),
    (1, 'Sub Genre', 'Cinema & Broadcast', 4.2, 3),
    (1, 'Type', 'Kindle Edition', 2.9, 4),
    (1, 'Author', 'Khaled Hosseini', 4.7, 2),
    
    -- Пользователь 2
    (2, 'Main Genre', 'Crime, Thriller & Mystery', 4.1, 7),
    (2, 'Sub Genre', 'Architecture', 3.5, 2),
    (2, 'Type', 'Paperback', 3.2, 8),
    (2, 'Author', 'Arthur Conan Doyle', 4.8, 3),
    
    -- Пользователь 3
    (3, 'Main Genre', 'Travel', 4.5, 6),
    (3, 'Sub Genre', 'Travel & Holiday Guides', 4.3, 4),
    (3, 'Type', 'Paperback', 3.7, 5),
    (3, 'Author', 'Anirban Mahapatra', 4.2, 1);

-- Тестовые глобальные предпочтения
INSERT INTO global_preferences (category, value, avg_weight, count) VALUES
    ('Main Genre', 'Arts, Film & Photography', 3.9, 150),
    ('Main Genre', 'Crime, Thriller & Mystery', 4.0, 180),
    ('Main Genre', 'Travel', 4.2, 120),
    ('Sub Genre', 'Cinema & Broadcast', 3.8, 90),
    ('Sub Genre', 'Architecture', 3.6, 70),
    ('Sub Genre', 'Travel & Holiday Guides', 4.1, 110),
    ('Type', 'Kindle Edition', 3.0, 200),
    ('Type', 'Paperback', 3.5, 350),
    ('Type', 'Poster', 2.8, 30),
    ('Author', 'Khaled Hosseini', 4.5, 65),
    ('Author', 'Arthur Conan Doyle', 4.6, 78),
    ('Author', 'Anirban Mahapatra', 4.0, 42);

-- Тестовые глобальные счетчики
INSERT INTO global_counts (category, value, total_count) VALUES
    ('Main Genre', 'Arts, Film & Photography', 420),
    ('Main Genre', 'Crime, Thriller & Mystery', 380),
    ('Main Genre', 'Travel', 290),
    ('Sub Genre', 'Cinema & Broadcast', 210),
    ('Sub Genre', 'Architecture', 150),
    ('Sub Genre', 'Travel & Holiday Guides', 230),
    ('Type', 'Kindle Edition', 480),
    ('Type', 'Paperback', 720),
    ('Type', 'Poster', 85),
    ('Author', 'Khaled Hosseini', 180),
    ('Author', 'Arthur Conan Doyle', 250),
    ('Author', 'Anirban Mahapatra', 120);

-- Тестовые векторные представления книг (пример с 5-мерными векторами для простоты)
INSERT INTO book_embeddings (book_title, embedding) VALUES
    ('The Kite Runner', '{0.42, 0.18, -0.32, 0.85, -0.15}'),
    ('Black Holes (L) : The Reith Lectures', '{-0.21, 0.65, 0.33, -0.12, 0.77}'),
    ('The Complete Novel of Sherlock Holmes', '{0.55, 0.23, -0.67, 0.12, 0.45}'),
    ('The Science of Storytelling', '{0.33, -0.45, 0.67, -0.28, 0.19}'),
    ('Lonely Planet India 19', '{0.12, 0.89, 0.32, -0.54, -0.23}');

-- Тестовые векторные профили пользователей
INSERT INTO user_embeddings (user_id, embedding) VALUES
    (1, '{0.35, 0.28, -0.22, 0.65, 0.12}'),
    (2, '{0.42, 0.15, -0.52, 0.08, 0.33}'),
    (3, '{0.18, 0.75, 0.22, -0.44, -0.15}');

-- Тестовые взаимодействия с книгами
INSERT INTO user_book_interactions (user_id, book_title, interaction_type, rating) VALUES
    (1, 'The Kite Runner', 'purchase', NULL),
    (1, 'The Kite Runner', 'rate', 4.5),
    (1, 'Black Holes (L) : The Reith Lectures', 'view', NULL),
    (1, 'Black Holes (L) : The Reith Lectures', 'purchase', NULL),
    (2, 'The Complete Novel of Sherlock Holmes', 'purchase', NULL),
    (2, 'The Complete Novel of Sherlock Holmes', 'rate', 5.0),
    (2, 'The Science of Storytelling', 'view', NULL),
    (3, 'Lonely Planet India 19', 'view', NULL),
    (3, 'Lonely Planet India 19', 'purchase', NULL),
    (3, 'Lonely Planet India 19', 'rate', 4.2);

-- Тестовые записи истории рекомендаций
INSERT INTO recommendation_history (user_id, book_title, recommendation_source) VALUES
    (1, 'Greenlights: Raucous stories and outlaw wisdom', 'content_based'),
    (1, 'The Science of Storytelling', 'collaborative_filtering'),
    (2, 'Black Holes (L) : The Reith Lectures', 'hybrid'),
    (2, 'Lonely Planet Australia', 'content_based'),
    (3, 'Insight Guides Poland', 'collaborative_filtering'),
    (3, 'Eyewitness Travel Phrase Book French', 'content_based');
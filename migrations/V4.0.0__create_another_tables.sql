-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица избранных книг пользователя
CREATE TABLE IF NOT EXISTS user_favorite_books (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    book_title VARCHAR(255) NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, book_title)
);

-- Таблица для хранения весов предпочтений пользователя по разным категориям
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id INTEGER NOT NULL,
    category VARCHAR(50) NOT NULL,    -- 'Main Genre', 'Sub Genre', 'Type', 'Author'
    value TEXT NOT NULL,              -- Конкретное значение категории
    weight FLOAT NOT NULL,            -- Вес предпочтения
    count INTEGER NOT NULL DEFAULT 1, -- Количество встречаемости этого значения
    PRIMARY KEY (user_id, category, value),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Таблица глобальных весов предпочтений (для новых пользователей)
CREATE TABLE IF NOT EXISTS global_preferences (
    category VARCHAR(50) NOT NULL,
    value TEXT NOT NULL,
    avg_weight FLOAT NOT NULL,        -- Средний вес предпочтений
    count INTEGER NOT NULL DEFAULT 0, -- Количество пользователей
    PRIMARY KEY (category, value)
);

-- Таблица глобальных подсчетов встречаемости значений
CREATE TABLE IF NOT EXISTS global_counts (
    category VARCHAR(50) NOT NULL,
    value TEXT NOT NULL,
    total_count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (category, value)
);

-- Таблица для хранения векторных представлений книг (UMAP embeddings)
CREATE TABLE IF NOT EXISTS book_embeddings (
    book_title VARCHAR(255) PRIMARY KEY,
    embedding FLOAT[] NOT NULL -- Массив с векторным представлением книги
);

-- Таблица для хранения векторного профиля пользователя
CREATE TABLE IF NOT EXISTS user_embeddings (
    user_id INTEGER PRIMARY KEY,
    embedding FLOAT[] NOT NULL, -- Профиль пользователя на основе прочитанных книг
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Таблица для отслеживания взаимодействий пользователя с книгами
CREATE TABLE IF NOT EXISTS user_book_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    book_title VARCHAR(255) NOT NULL,
    interaction_type VARCHAR(50) NOT NULL, -- 'view', 'like', 'purchase', 'rate', etc.
    rating FLOAT, -- оценка, если пользователь оценил книгу
    interaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Таблица для хранения истории рекомендаций
CREATE TABLE IF NOT EXISTS recommendation_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    book_title VARCHAR(255) NOT NULL,
    recommendation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recommendation_source VARCHAR(100), -- метод, использованный для рекомендации
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
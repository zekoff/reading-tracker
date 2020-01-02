DROP TABLE IF EXISTS Readings2020;

CREATE TABLE Readings2020 (
    id SERIAL PRIMARY KEY,
    passage TEXT,
    reading_day INTEGER,
    week INTEGER,
    start_day TEXT,
    end_day TEXT
);
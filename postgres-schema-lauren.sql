DROP TABLE IF EXISTS Readings2020lauren;

CREATE TABLE Readings2020lauren (
    id SERIAL PRIMARY KEY,
    passage TEXT,
    reading_day INTEGER,
    week INTEGER,
    start_day TEXT,
    end_day TEXT,
    completed TEXT
);
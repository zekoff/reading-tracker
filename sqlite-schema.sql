DROP TABLE IF EXISTS Readings;

CREATE TABLE Readings (
    id INTEGER PRIMARY KEY,
    passage TEXT,
    time_min INTEGER,
    week TEXT,
    original_row INTEGER
);
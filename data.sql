


CREATE TABLE IF NOT EXISTS Movies(
    movie_id INTEGER PRIMARY KEY  AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    genre TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    STATUS TEXT DEFAULT 'active'  CHECK(STATUS IN('active','inactive','archived'))
);

CREATE TABLE IF NOT EXISTS Theaters(
    theater_id INTEGER Primary KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT ,
    STATUS TEXT DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'maintenance')),
    capacity INTEGER CHECK(capacity>0)
);


CREATE TABLE IF NOT EXISTS Critics(
    critics_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    publication TEXT,
    STATUS TEXT DEFAULT 'active' CHECK(STATUS IN('active','banned','retired'))
);



CREATE TABLE Screenings (
    screening_id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    theater_id INTEGER NOT NULL,
    show_time DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
    FOREIGN KEY (theater_id) REFERENCES Theaters(theater_id)
);

CREATE TABLE Reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    critic_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL CHECK(rating >= 1.0 AND rating <= 10.0),
    comment TEXT,
    review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(critic_id) REFERENCES Critics(critic_id),
    FOREIGN KEY(movie_id) REFERENCES Movies(movie_id),
    UNIQUE(critic_id, movie_id) -- prevents duplicate reviews by same critic
);

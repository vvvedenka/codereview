DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'vvvedenka') THEN
      CREATE DATABASE vvvedenka;
   END IF;
END
$$;

\c vvvedenka;

CREATE TABLE IF NOT EXISTS words (
    id SERIAL PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    is_rare BOOLEAN DEFAULT FALSE,
    length INTEGER NOT NULL,
    syllables INTEGER NOT NULL
);

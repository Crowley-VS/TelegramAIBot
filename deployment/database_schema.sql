-- Table: characters
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    conversation_id BIGINT,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- Table: characters
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    conversation_id INTEGER,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- Table: messages
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

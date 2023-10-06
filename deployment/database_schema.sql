-- Table: conversations
CREATE TABLE conversations (
    id BIGINT PRIMARY KEY, -- Use BIGINT to store the original Telegram chat ID
    tokens INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table: characters
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    conversation_id BIGINT, -- Use BIGINT to reference the original Telegram chat ID
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- Table: messages
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id BIGINT NOT NULL, -- Use BIGINT to reference the original Telegram chat ID
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

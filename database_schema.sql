-- Create credit_cards table
CREATE TABLE credit_cards (
    id INTEGER PRIMARY KEY,
    apr FLOAT,
    benefits JSON,
    credit_needed JSON,
    issuer VARCHAR,
    name VARCHAR,
    reward_category_map JSON
);

-- Create cc_assoc table
CREATE TABLE cc_assoc (
    last_update DATE,
    credit_card_id INTEGER,
    PRIMARY KEY (last_update, credit_card_id),
    FOREIGN KEY (credit_card_id) REFERENCES credit_cards(id)
);

-- Create Users table
CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    disabled BOOLEAN,
    email VARCHAR,
    full_name VARCHAR,
    hashed_password VARCHAR,
    username VARCHAR
);

-- Create Accounts table
CREATE TABLE Accounts (
    id VARCHAR PRIMARY KEY,
    currency VARCHAR,
    enrollment_id VARCHAR,
    institution_id VARCHAR,
    institution_name VARCHAR,
    last_four VARCHAR,
    last_update DATE,
    name VARCHAR,
    status VARCHAR,
    subtype VARCHAR,
    type VARCHAR,
    FOREIGN KEY (enrollment_id) REFERENCES enrollment(since)
);

-- Create enrollment table
CREATE TABLE enrollment (
    since DATE PRIMARY KEY
);

-- Create preference_association table
CREATE TABLE preference_association (
    user_id INTEGER PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Create travel_preference table
CREATE TABLE travel_preference (
    user_id INTEGER PRIMARY KEY,
    avoid_airlines JSON,
    desired_airlines JSON,
    frequent_travel_destinations JSON,
    preferred_airlines JSON,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Create consumer_preference table
CREATE TABLE consumer_preference (
    user_id INTEGER PRIMARY KEY,
    favorite_restaurants JSON,
    favorite_stores JSON,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Create bank_preference table
CREATE TABLE bank_preference (
    user_id INTEGER PRIMARY KEY,
    avoid_banks JSON,
    have_banks JSON,
    preferred_banks JSON,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Create business_preference table
CREATE TABLE business_preference (
    user_id INTEGER PRIMARY KEY,
    business_size VARCHAR,
    business_type JSON,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Create credit_preference table
CREATE TABLE credit_preference (
    user_id INTEGER PRIMARY KEY,
    credit_score INTEGER,
    lifestyle VARCHAR,
    salary INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Create Transactions table
CREATE TABLE Transactions (
    txn_id VARCHAR PRIMARY KEY,
    category VARCHAR,
    counterpart_id INTEGER,
    processing_status VARCHAR,
    FOREIGN KEY (counterpart_id) REFERENCES Counterparty(id)
);

-- Create Transaction Details table
CREATE TABLE Transaction_Details (
    txn_id VARCHAR,
    category VARCHAR,
    counterpart_id INTEGER,
    processing_status VARCHAR,
    PRIMARY KEY (txn_id, counterpart_id),
    FOREIGN KEY (txn_id) REFERENCES Transactions(txn_id),
    FOREIGN KEY (counterpart_id) REFERENCES Counterparty(id)
);

-- Create Counterparty table
CREATE TABLE Counterparty (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    type VARCHAR
);

-- Create counter_association table
CREATE TABLE counter_association (
    txn_id VARCHAR,
    counterparty_id INTEGER,
    PRIMARY KEY (txn_id, counterparty_id),
    FOREIGN KEY (txn_id) REFERENCES Transactions(txn_id),
    FOREIGN KEY (counterparty_id) REFERENCES Counterparty(id)
);

-- Create enrollment relationship table
CREATE TABLE enrollment (
    since DATE,
    user_id INTEGER,
    account_id VARCHAR,
    PRIMARY KEY (since, user_id, account_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (account_id) REFERENCES Accounts(id)
);

-- Create cc_assoc relationship table
CREATE TABLE cc_assoc (
    last_update DATE,
    credit_card_id INTEGER,
    PRIMARY KEY (last_update, credit_card_id),
    FOREIGN KEY (credit_card_id) REFERENCES credit_cards(id)
);

-- Create preference_association relationship table
CREATE TABLE preference_association (
    user_id INTEGER,
    travel_preference_id INTEGER,
    consumer_preference_id INTEGER,
    bank_preference_id INTEGER,
    business_preference_id INTEGER,
    credit_preference_id INTEGER,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (travel_preference_id) REFERENCES travel_preference(user_id),
    FOREIGN KEY (consumer_preference_id) REFERENCES consumer_preference(user_id),
    FOREIGN KEY (bank_preference_id) REFERENCES bank_preference(user_id),
    FOREIGN KEY (business_preference_id) REFERENCES business_preference(user_id),
    FOREIGN KEY (credit_preference_id) REFERENCES credit_preference(user_id)
);

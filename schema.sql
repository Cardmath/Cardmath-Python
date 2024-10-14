
CREATE TABLE counterparty (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	type VARCHAR, 
	PRIMARY KEY (id)
)




CREATE TABLE credit_cards (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	issuer VARCHAR, 
	reward_category_map JSON, 
	benefits JSON, 
	credit_needed JSON, 
	apr FLOAT, 
	PRIMARY KEY (id)
)




CREATE TABLE transactions (
	txn_id VARCHAR NOT NULL, 
	account_id VARCHAR NOT NULL, 
	amount FLOAT NOT NULL, 
	date DATE NOT NULL, 
	description VARCHAR NOT NULL, 
	status VARCHAR NOT NULL, 
	running_balance FLOAT, 
	type VARCHAR NOT NULL, 
	PRIMARY KEY (txn_id)
)




CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	full_name VARCHAR, 
	disabled BOOLEAN, 
	hashed_password VARCHAR NOT NULL, 
	PRIMARY KEY (id)
)




CREATE TABLE cardratings_scrape (
	scrape_id INTEGER NOT NULL, 
	credit_cards_id INTEGER, 
	name VARCHAR, 
	description_used INTEGER, 
	unparsed_issuer VARCHAR, 
	unparsed_credit_needed VARCHAR, 
	unparsed_card_attributes VARCHAR, 
	PRIMARY KEY (scrape_id), 
	FOREIGN KEY(credit_cards_id) REFERENCES credit_cards (id)
)




CREATE TABLE enrollments (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	access_token VARCHAR NOT NULL, 
	enrollment_id VARCHAR NOT NULL, 
	institution_name VARCHAR NOT NULL, 
	signatures JSON NOT NULL, 
	last_updated DATE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)




CREATE TABLE preferences (
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)




CREATE TABLE transaction_details (
	txn_id VARCHAR NOT NULL, 
	counterparty_id INTEGER, 
	processing_status VARCHAR NOT NULL, 
	category VARCHAR, 
	PRIMARY KEY (txn_id), 
	FOREIGN KEY(txn_id) REFERENCES transactions (txn_id), 
	FOREIGN KEY(counterparty_id) REFERENCES counterparty (id)
)




CREATE TABLE user_credit_card_association (
	user_id INTEGER NOT NULL, 
	credit_card_id INTEGER NOT NULL, 
	PRIMARY KEY (user_id, credit_card_id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(credit_card_id) REFERENCES credit_cards (id)
)




CREATE TABLE accounts (
	id VARCHAR NOT NULL, 
	enrollment_id VARCHAR NOT NULL, 
	institution_name VARCHAR NOT NULL, 
	institution_id VARCHAR NOT NULL, 
	type VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	subtype VARCHAR NOT NULL, 
	currency VARCHAR NOT NULL, 
	last_four VARCHAR NOT NULL, 
	last_updated DATE NOT NULL, 
	status VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(enrollment_id) REFERENCES enrollments (enrollment_id)
)




CREATE TABLE banks_preferences (
	user_id INTEGER NOT NULL, 
	have_banks JSON, 
	preferred_banks JSON, 
	avoid_banks JSON, 
	PRIMARY KEY (user_id), 
	FOREIGN KEY(user_id) REFERENCES preferences (user_id)
)




CREATE TABLE business_preferences (
	user_id INTEGER NOT NULL, 
	business_type JSON, 
	business_size VARCHAR, 
	PRIMARY KEY (user_id), 
	FOREIGN KEY(user_id) REFERENCES preferences (user_id)
)




CREATE TABLE consumer_preferences (
	user_id INTEGER NOT NULL, 
	favorite_restaurants JSON, 
	favorite_stores JSON, 
	PRIMARY KEY (user_id), 
	FOREIGN KEY(user_id) REFERENCES preferences (user_id)
)




CREATE TABLE credit_profile_preferences (
	user_id INTEGER NOT NULL, 
	credit_score INTEGER, 
	salary INTEGER, 
	lifestyle VARCHAR, 
	PRIMARY KEY (user_id), 
	FOREIGN KEY(user_id) REFERENCES preferences (user_id)
)




CREATE TABLE travel_preferences (
	user_id INTEGER NOT NULL, 
	preferred_airlines JSON, 
	avoid_airlines JSON, 
	frequent_travel_destinations JSON, 
	desired_benefits JSON, 
	PRIMARY KEY (user_id), 
	FOREIGN KEY(user_id) REFERENCES preferences (user_id)
)




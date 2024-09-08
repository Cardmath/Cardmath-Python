from .dbinterface import DatabaseInterface
from creditcard import CreditCard
import sqlite3

class SQLiteImpl(DatabaseInterface):
    
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()
            
    def is_empty(self, table_name: str = 'unparsed_data'):
        query = f'SELECT COUNT(*) FROM {table_name}'
        result = self.cursor.execute(query)
        self.conn.commit()
        return result.fetchone()[0] == 0
    
    def count_rows(self, table_name: str = 'unparsed_data'):
        query = f'SELECT COUNT(*) FROM {table_name}'
        result = self.cursor.execute(query)
        self.conn.commit()
        return result.fetchone()[0]

    def create_unparsed_data_table(self, cc_dict: dict = None):
        query = '''
        CREATE TABLE IF NOT EXISTS unparsed_data (
            id INTEGER PRIMARY KEY,
            name TEXT,
            issuer TEXT,
            score_needed TEXT,
            description_used INTEGER,
            attributes TEXT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

    def create_parsed_data_table(self, cc_list: list = None):
        query = '''
        CREATE TABLE IF NOT EXISTS parsed_data (
            id INTEGER PRIMARY KEY,
            name TEXT,
            issuer TEXT,
            reward_category_map TEXT,
            benefits TEXT,
            credit_needed TEXT,
            apr REAL
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

    def update_unparsed_data_table_entry(self, entry_id, name, issuer, score_needed, attributes, description_used):
        query = f'''
        INSERT INTO unparsed_data (id, name, issuer, score_needed, attributes, description_used)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (entry_id, name, issuer, score_needed, attributes, description_used))
        self.conn.commit()

    def update_parsed_data_table_entry(self, cc: CreditCard = None):
        query = '''
        INSERT INTO parsed_data (name, issuer, reward_category_map, benefits, credit_needed, apr)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (cc.name, cc.issuer.value, str(cc.reward_category_map), str([benefit.value for benefit in cc.benefits]), str(cc.credit_needed), cc.apr))
        self.conn.commit()

    def delete_unparsed_data_table_entry(self, condition):
        query = f'DELETE FROM unparsed_data WHERE {condition}'
        self.cursor.execute(query)
        self.conn.commit()

    def delete_parsed_data_table_entry(self, condition):
        query = f'DELETE FROM parsed_data WHERE {condition}'
        self.cursor.execute(query)
        self.conn.commit()

    def query_unparsed_data(self, condition=None):
        query = 'SELECT * FROM unparsed_data'
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def query_parsed_data(self, condition=None):
        query = 'SELECT id, name, issuer, score_needed, description_used, attributes FROM parsed_data'
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

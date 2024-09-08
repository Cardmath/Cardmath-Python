from abc import ABC, abstractmethod

class DatabaseInterface(ABC):   
    
    @abstractmethod
    def connect(self, db_name: str):
        pass
    
    @abstractmethod
    def close(self):
        pass
    
    @abstractmethod
    def create_unparsed_data_table(self, cc_dict=None):
        pass
    
    @abstractmethod
    def update_unparsed_data_table_entry(self, cc=None):
        pass
    
    @abstractmethod
    def create_parsed_data_table(self, cc_list=None):
        pass
    
    @abstractmethod
    def update_parsed_data_table_entry(self, cc_object=None):
        pass
    
    @abstractmethod
    def delete_unparsed_data_table_entry(self, condition):
        pass
    
    @abstractmethod
    def delete_parsed_data_table_entry(self, condition):
        pass
    
    @abstractmethod
    def query_unparsed_data(self, condition=None):
        pass
    
    @abstractmethod
    def query_parsed_data(self, condition=None):
        pass
    
    @abstractmethod
    def commit(self):
        pass
    
    @abstractmethod
    def rollback(self):
        pass
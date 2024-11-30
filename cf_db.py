"""
This script creates DuckDB database
"""
import duckdb
from constants import DATABASE_PATH

''' implement a context manager '''
class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
    
    def __enter__(self):
        self.connection = duckdb.connect(self.db_path)
        return self
    
    def query(self, query):
        return self.connection.execute(query).fetchall() # fetchall() return a list

    def __exit__(self, exc_type, exc_value, traceback): # params are to handle exceptions
        if self.connection:
            self.connection.close()

if __name__ == '__main__':
    with Database(DATABASE_PATH) as db: # with statement opens the db
        query1 = db.query("select * from information_schema.schemata;")
    print(query1)



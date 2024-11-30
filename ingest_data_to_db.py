"""
This script ingests the csv files into cd_db database
"""
from constants import DATABASE_PATH, DATA_PATH
from cf_db import Database
from pathlib import Path
import duckdb

con = duckdb.connect(str(DATABASE_PATH))
for csv in ['holidays_events.csv', 'items.csv', 'oil.csv', 'stores.csv', 'train.csv', 'transactions.csv']:
    table = csv[:-4]
    # existing_tables = con.sql("SHOW TABLES")
    query_table_exists = \
        f"""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{table}'
        """
    if con.sql(query_table_exists).fetchone()[0] == 0:
        query_ingest = \
            f"""
            CREATE TABLE {table} AS
            SELECT * FROM '{DATA_PATH}/{csv}'
            """
        con.sql(query_ingest)
    else:   print(f"Table '{table}' already exists; skipping ingestion.")



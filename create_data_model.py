"""
This script creates the rest of the tables and views for the Power BI data model
and contains some queries for EDA.
"""
from constants import DATABASE_PATH
from cf_db import Database
import duckdb

con = duckdb.connect(str(DATABASE_PATH))

"""
items table: title-case family column; rename columns
"""
items_df = con.sql('SELECT * FROM items').df()
items_df.loc[items_df.family=='LIQUOR,WINE,BEER', 'family'] = 'Liquor, Wine, Beer'
items_df.family = (items_df.family).str.title()
items_df.loc[items_df.family=='Grocery Ii', 'family'] = 'Grocery II'
items_df.loc[items_df.family=='Home And Kitchen I', 'family'] = 'Home and Kitchen I'
items_df.loc[items_df.family=='Home And Kitchen Ii', 'family'] = 'Home and Kitchen II'
items_df.loc[items_df.family=='Lawn And Garden', 'family'] = 'Lawn and Garden'
items_df.loc[items_df.family=='Players And Electronics', 'family'] = 'Players and Electronics'
items_df.loc[items_df.family=='School And Office Supplies', 'family'] = 'School and Office Supplies'


con.register("items_temp", items_df)
con.sql("""
        DROP TABLE IF EXISTS items;
        CREATE TABLE items AS
        SELECT item_nbr AS "Item ID", family as Category,
            class as Class, 
            CASE WHEN perishable = 1 THEN 'Perishable' ELSE 'Non-Perishable' END AS Perishable
        FROM items_temp
        """)
con.unregister("items_temp")


"""
train table: 
    1. Count the number of null, true, and false values in the onpromotion column.
    2. Find date range for non-null values for the onpromotion column.
    3. Rename columns.
    4. Confirm how many null values in the "On Promotion" column from 2014-04-01 and later,
       which is when we starting having non-null values in "On Promotion" column. Confirmed
       that there are no null values in this date range.
    5. Create train_view with date range starting at 2014-04-01.
"""
con.sql("""
        SELECT 
            SUM(CASE WHEN onpromotion IS NULL THEN 1 ELSE 0 END) AS null_count,
            SUM(CASE WHEN onpromotion = 'True' THEN 1 ELSE 0 END) AS true_count,
            SUM(CASE WHEN onpromotion = 'False' THEN 1 ELSE 0 END) AS false_count
        FROM train
        """)
        
con.sql("""
        SELECT MIN(date), MAX(date), onpromotion
        FROM train 
        WHERE onpromotion IS NOT NULL GROUP BY onpromotion
        """)

con.sql("""
        ALTER TABLE train RENAME COLUMN id TO "Train ID";
        ALTER TABLE train RENAME COLUMN date TO Date;
        ALTER TABLE train RENAME COLUMN store_nbr TO "Store ID";
        ALTER TABLE train RENAME COLUMN item_nbr TO "Item ID";
        ALTER TABLE train RENAME COLUMN unit_sales TO "Unit Sales";
        ALTER TABLE train RENAME COLUMN onpromotion TO "On Promotion";
        """)

con.sql("""SELECT * FROM train WHERE "On Promotion" IS NULL AND Date >= DATE '2014-04-01'""")

con.sql("""
        DROP VIEW IF EXISTS train_view;
        CREATE VIEW train_view AS 
        SELECT "Train ID", Date, "Store ID", "Item ID", "Unit Sales",
            CASE WHEN "On Promotion" = 'True' THEN 'Yes' ELSE 'No' END AS "On Promotion"
        FROM train
        WHERE Date >= DATE '2014-04-01';
        SELECT "On Promotion", COUNT("On Promotion") FROM train_view GROUP BY "On Promotion";
        """)


""" holidays_events table: rename columns """
con.sql("""
        ALTER TABLE holidays_events RENAME COLUMN date TO Date;
        ALTER TABLE holidays_events RENAME COLUMN type TO Type;
        ALTER TABLE holidays_events RENAME COLUMN locale TO Locale;
        ALTER TABLE holidays_events RENAME COLUMN locale_name TO "Locale Name";
        ALTER TABLE holidays_events RENAME COLUMN description TO Description;
        ALTER TABLE holidays_events RENAME COLUMN transferred TO Transferred;
        """)


"""
transactions table: rename columns
transactions_view: add "Store ID" and "On Promotion" data to transactions table by joining
with train table.
"""
con.sql("""
        ALTER TABLE transactions RENAME COLUMN date TO Date;
        ALTER TABLE transactions RENAME COLUMN store_nbr TO "Store ID";
        ALTER TABLE transactions RENAME COLUMN transactions TO Transactions;
        """)

con.sql("""
        DROP VIEW IF EXISTS transactions_view;
        CREATE VIEW transactions_view AS
        WITH train_agg AS (
            SELECT Date, "Store ID", SUM("Unit Sales") AS "Unit Sales"
            FROM train
            GROUP BY Date, "Store ID")
        SELECT transactions.Date, transactions."Store ID", transactions.Transactions,
            train_agg."Unit Sales"
        FROM train_agg
        JOIN transactions
            ON train_agg.Date  = transactions.Date AND train_agg."Store ID" = transactions."Store ID"
        WHERE transactions.Date >= DATE '2014-04-01'
        ORDER BY transactions.Date, transactions."Store ID";
        """)


""" stores table: rename columns; add Country column """
con.sql("""
        ALTER TABLE stores RENAME COLUMN store_nbr TO "Store ID";
        ALTER TABLE stores RENAME COLUMN city TO City;
        ALTER TABLE stores RENAME COLUMN state TO State;
        ALTER TABLE stores RENAME COLUMN type TO Type;
        ALTER TABLE stores RENAME COLUMN cluster TO Cluster;
        """)

con.sql("""
        ALTER TABLE stores ADD COLUMN Country VARCHAR;
        UPDATE stores SET Country = 'Ecuador';
        """)


""" Export tables and views as csv files """
con.execute("""
            COPY dates TO 'dates_pbi.csv' (HEADER, DELIMITER ',');
            COPY items TO 'items_pbi.csv' (HEADER, DELIMITER ',');
            COPY oil_imputed TO 'oil_pbi.csv' (HEADER, DELIMITER ',');
            COPY stores TO 'stores_pbi.csv' (HEADER, DELIMITER ',');
            COPY train_view TO 'train_pbi.csv' (HEADER, DELIMITER ',');
            COPY transactions_view TO 'transactions_pbi.csv' (HEADER, DELIMITER ',');
            """)













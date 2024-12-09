"""
This script creates and transforms views in cf_db; also creates dates table so that
oil table (oil_dates) contains every date in date range.
"""
from constants import DATABASE_PATH, DATA_PATH
from cf_db import Database
from pathlib import Path
import duckdb
import pandas as pd
import numpy as np

con = duckdb.connect(str(DATABASE_PATH))

"""
Date table:
    1. Contains date range of truncated train table (2014-05-01 to 2016-06-30).
    2. Create additional columns for month name, month, year, quarter, start of week date,
       start of month, start of quarter, and start of year.
"""
con.sql("""
        DROP TABLE IF EXISTS dates;
        CREATE TABLE dates AS (
        	WITH dates_cte AS (
        		SELECT UNNEST(GENERATE_SERIES('2014-05-01'::DATE, '2016-07-31'::DATE, '1 day'::INTERVAL)) AS date
        	)
        	SELECT date::DATE AS Date,
        		 STRFTIME(date, '%B') AS "Month Name",
        		 EXTRACT (MONTH FROM date) AS "Month",
        		 EXTRACT (YEAR FROM date) AS "Year",
        		 CASE WHEN EXTRACT (MONTH FROM date) IN (1, 2, 3) THEN 'Q1'
        			  WHEN EXTRACT (MONTH FROM date) IN (4, 5, 6) THEN 'Q2'
        			  WHEN EXTRACT (MONTH FROM date) IN (7, 8, 9) THEN 'Q3'
        			  ELSE 'Q4' 
        			  END	AS "Quarter",
        		 (DATE_TRUNC('week', date) - INTERVAL '1 day')::DATE AS "Week Start", -- Set Sunday as start of week
        		 DATE_TRUNC('month', date)::DATE AS "Month Start",
        	    DATE_TRUNC('quarter', date)::DATE AS "Quarter Start",
        	    DATE_TRUNC('year', date)::DATE AS "Year Start"
        	FROM dates_cte
        );
        """)


""" 
Transform oil table: impute missing prices; rename columns
"""
con.sql("""
        DROP TABLE IF EXISTS oil_dates;
        CREATE TABLE oil_dates AS 
        SELECT d.*, o.*
        FROM dates d
        LEFT JOIN oil o
            ON d.Date = o.date
        ORDER BY d.Date;
        SELECT * FROM oil_dates LIMIT 10;
        """)


""" 
Transform oil_dates table: impute missing prices; rename columns.
Output is oil_imputed table.
"""
oil_df = con.sql("SELECT * FROM oil_dates").df()
oil_df = oil_df.sort_values(by='Date')
def impute_missing_prices(df):
    """
    Parameters
    ----------
    df : Pandas dataframe. Column-1 is date type or an ordinal data type. Column-2 is 
        float type. Column-2 (oil prices) has some missing values. This function imputes 
        them with the average of the nearest available value before and after the missing 
        value. If there are consecutive missing values, all of them are replaced with the 
        average of the nearest available value before and after these missing values.
        If there are (consecutive) missing value(s) at the start of the data frame, they 
        are imputed with the next available value. If there are (consecutive) 
        missing value(s) at the end of the data frame, they are imputed with the
        preceding available value.

    Returns
    -------
    df : original df with missing values imputed as described above.

    """
    prices = np.array(df['dcoilwtico'])
    first_valid_index = np.argmax(~np.isnan(prices))
    if first_valid_index > 0:
        prices[:first_valid_index] = prices[first_valid_index]
    last_valid_index = len(prices) - 1 - np.argmax(~np.isnan(prices[::-1]))
    if last_valid_index < len(prices) - 1:
        prices[last_valid_index+1:] = prices[last_valid_index]
    
    null_index = np.where(np.isnan(prices))[0]
    i = 0
    while i < len(null_index):
        j = i
        k = null_index[j]
        prev_valid_value = prices[null_index[j]-1]
        try:
            if null_index[j]+1 == null_index[j+1]:
                k = null_index[j]
                try:
                    while null_index[j]+1 == null_index[j+1]:
                        j += 1
                except: pass
        except:
            k = null_index[j]
        next_valid_value = prices[null_index[j]+1]
        prices[k:null_index[j]+1] = round(np.mean((prev_valid_value, next_valid_value)), 2)
        i = j+1
    df['dcoilwtico'] = prices
    return df

oil_imputed_df = impute_missing_prices(oil_df)

con.register("oil_temp", oil_imputed_df)
con.sql("""
        DROP TABLE IF EXISTS oil_imputed;
        CREATE TABLE oil_imputed AS
        SELECT date::DATE AS Date,
            dcoilwtico AS "Oil Price"
        FROM oil_temp
        """)
con.unregister("oil_temp")





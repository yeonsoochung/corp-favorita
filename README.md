# Corporación Favorita
## Analysis of on-promo sales at a large Ecuadorian grocery chain.

Corporación Favorita provided sales data ranging from 2013 to 2017. The data includes information on stores, items, number of units sold, number of items sold on promo, number of transactions at specifc store/date combos (but no transaction data at the itemized level), and oil prices, which have a significant impact on Ecuador's economy. The "On Promotion" data is given as True/False, and I filtered out its null values, which truncated the data set's date range to Apr. 2014 - Aug. 2017.

In this project, I analyzed the data pertaining to items sold on promo. I developed a Power BI dashboard that enables the user to view units sold over time and % of units sold on-promo over time. The dashboard's interactive features allow the user to analyze these trends based on item category, location, different time granularities, and comparing with oil prices.

I chose DuckDB as my database because, with Python, I was able to run SQL queries and code in Pandas to transform the data sets and create my data model for Power BI. One of my processing stages involved imputing missing values in the oil prices data table with the average of the nearest available values (nearest based on dates), and I decided that Pandas was the best tool to perform this.

Data source: https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting/data

## ELT Steps and Data Model

**cf_db.py:**  This script creates my DuckDB database.
**ingest_data_to_db.py:** After downloading the data set from Kaggle, I ingest the csv files into the database.
**impute_oil_table.py:** The raw oil table has columns for dates and oil prices (USD per barrel). Some prices have null values, and there are some dates that are skipped. This script does the following:
- Creates a date table for the range of my data set (Apr. 1, 2014 to Aug. 15, 2017).
- Join the table of continuous dates with the oil table.
- Imputes the null prices with the average of the nearest (in terms of dates) available prices before and after the missing value(s). If there are consecutive missing values, they are all imputed with the same average value. If there are (consecutive) missing values at the beginning of the table, they are imputed with the nearest available value. Likewise for for (consecutive) missing values at the end of the table.
- The processed oil table is saved as a new table in the database, with renamed columns.
**test_imputer.py:** Performs unit tests on the imputer function in **impute_oil_table.py**.
**create_data_model.py:** Sets up the rest of the data model:
- Performed a join operation to add a column for unit sales to the transactions data and created a view with the new table.
- Truncated the train table to only include dates for which "onpromotion" data is not null; and converted the "onpromotion" values of True/False to Yes/No.
- Renamed columns for all tables and views.
- I create a view for transactions in order to keep the original transactions table. I kept the other tables as tables because I did not create new columns with them - just made changes like imputations and renaming.



<p align="center">
<img src="images/ca-stores-rev.PNG" alt="Alt text" width="600"/>
</p>

# Corporación Favorita: Analysis of On-Promo Sales at a Large Ecuadorian Grocery Chain

Corporación Favorita provided sales data ranging from 2013 to 2017. The data includes information on stores, items, number of units sold, items sold on promo, number of transactions at specific store/date pairs (no transaction data at the itemized level nor revenue data, unfortunately), and oil prices, which have a significant impact on Ecuador's economy. The "On Promotion" data is given as True/False, and I filtered out its null values, which were all in the first year or so of the data set, thus truncating the data set's date range to Apr. 2014 - Aug. 2017. Due to Power BI Service's free-tier limit of 1 GB for publised reports, the data set was furter truncated to a data from of Apr. 2014 - Jul. 2016.

In this project, I analyzed the data pertaining to items sold on promo. I developed a Power BI dashboard that enables the user to view units sold over time and % of units sold on-promo over time. The dashboard's interactive features allow the user to analyze these trends based on item category, location, date range, different time granularities (month, quarter, and year), and comparison with oil prices. The second page of my dashboard quantifies the visual trends displayed in the first page.

I chose DuckDB as my database because, with Python, I was able to run SQL queries and code in Pandas to transform the data sets and create my data model for Power BI. One of my processing stages involved imputing missing values in the oil prices data table with the average of the nearest available values (nearest based on dates), and I decided that Pandas was the most efficient tool to perform this with.

DAX queries were implemented in Power BI to create aggregate measures/metrics.

My Power BI report can be viewed here: https://app.powerbi.com/view?r=eyJrIjoiYjA3ZjBlZmUtMTg4YS00ZDcyLWEwYWMtMDgxNWU5YTE1N2VjIiwidCI6ImJlMjI4MDdiLTI1OTEtNDBkNy1iYmI2LTBkYTg0ZDMxYWNmNyIsImMiOjN9

Its pbix file can be downloaded here: https://drive.google.com/file/d/1jzEJcYnCsVPzPH8_M60Z1OgxVPVRn2Ss

Data source: https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting/data

## Summary of Findings

I decided to focus on two metrics in this analysis of on-promo sales: units sold and % units sold on-promo. Total unit sales reflect the overall health of the company, and % units sold on-promo indicate the proportion of items on promotion. I am interested in how these two metrics trend over time and how they relate to store locations and oil prices.

The total number of units sold across all stores averaged at about 18MM units from April 2014 to June 2015. After June 2015, unit sales increased to a higher average of about 24MM units. This shift coincides with oil prices decreasing and staying at a lower range than 2014 levels.

<p align="center">
<img src="images/dashboard1.PNG" alt="Alt text" width="1000"/>
</p>

<p align="center">
<img src="images/dashboard2.PNG" alt="Alt text" width="1000"/>
</p>

Note that the line charts can be drilled up/down to aggregate the measures by week, month, and year. The images in this README show the trends aggregated by month.

Overall trends demonstrate that the lower the price of oil, the higher the units sold as well as the share of units sold that were on promo. Ecuador is a petrostate, so if oil prices decrease, then consumers will be less likely to spend money, which is why we see more items sold on promotion.

Trends of unit sales at the state level generally mirrored the overall trend. The state of Santa Elena is an exception due to a substantial dip in sales after Apr. 2016. By contrast, its % unit sales on-promo saw a spike at around June 2016. The overlapping time periods indicate customers were particularly focused on purchasing items on promotion during this time period. Another exception is the trend in % unit sales on-promo in the state of Manabi. In May 2016, 99.92% of units sold were on-promo. This coincides with a major earthquake that occurred in this state on Apr. 16, 2016.

### Top Selling Items on-Promo

- **School and Office Supplies (SOS)** sell at the highest percentage of units on promo overall (i.e., entire data set), driven by their sales in Q2 and Q3 over every year in the data set (In Ecuador, schools in the coastal regions start the school year in April, and those in the Andean regions start in September). The steep drop in oil prices in Q2 of 2015 prompted Ecuadorians to withhold purchase of SOS items, indicated by the absence of a peak for the April 2015 back-to-school season.

<p align="center">
<img src="images/sos.PNG" alt="Alt text" width="800"/>
</p>

During Q1, "Home and Kitchen II", Meats, Produce, and Eggs have the highest percentage of unit sales from items on promo. In Q4, the leading categories are “Home and Kitchen II”, Frozen Foods, Produce, and Meats. There is some variation at the state level, but in most states, SOS items top the list followed by food-based categories.

- **Home and Kitchen II:** Unit sales generally increased as oil prices decreased after Jan. 2015, followed by stability in sales after Jan. 2016 as oil prices remained at low levels. Before 2016, however, there was a spike in units sold in Oct. 2015, and there were two spikes in % units sold (in June 2015 and Oct. 2015). The spikes suggest items were promoted to boost sales after oil prices dropped, resulting in higher levels of sales than 2014 (before oil prices fell) to bring back profitability. Increase in the sales of these items as well as food items compared to 2014 sales indicate more Ecuadorians were preparing meals at home. It would be interesting to see revenue and profit data for Corporación Favorita as well as item-level pricing data to analyze their promotional strategies.

<p align="center">
<img src="images/hk2.PNG" alt="Alt text" width="800"/>
</p>

- **Meats:** Unit sales of meat products decreased when oil prices fell in Fall 2014, but increased to relative stability in the middle of 2015.  % units sold on-promo stayed mostly consistent, except at the start of the data set.

<p align="center">
<img src="images/meats.PNG" alt="Alt text" width="800"/>
</p>

- **Produce:** Apart from an initial low and two sharp dips, unit sales and % units sold on-promo stay relatively consistent throughout the data set. The second sharp dip, starting at Jan. 2015, lasts for five months and coincides with a slide in oil prices that stabilize in those five months. Along with the necessity of buying produce, more of these items must have been promoted to bring profits back up, as oil prices did not climb back to their 2014 levels.

<p align="center">
<img src="images/produce.PNG" alt="Alt text" width="800"/>
</p>

- **Eggs:** There is a visually discernible correlation between egg sales and oil prices starting from Oct. 2014. The % of eggs sold on-promo was below 10% before oil prices started to fall in late 2014, after which it averaged around 17%.

<p align="center">
<img src="images/eggs.PNG" alt="Alt text" width="800"/>
</p>

## ELT Steps and Data Model

- **cf_db.py:**  This script creates my DuckDB database.

- **ingest_data_to_db.py:** After downloading the data set from Kaggle, I ingest the csv files into the database.

- **impute_oil_table.py:** The raw oil table has columns for dates and oil prices (USD per barrel). Some prices have null values, and there are some dates that are skipped. This script does the following:
  - Creates a date table for the range of my data set (Apr. 1, 2014 to Aug. 15, 2017).
  - Join the table of continuous dates with the oil table.
  - Imputes the null prices with the average of the nearest (in terms of dates) available prices before and after the missing value(s). If there are consecutive missing values, they are all imputed with the same average value. If there are (consecutive) missing values at the beginning of the table, they are imputed with the nearest available value. Likewise for for (consecutive) missing values at the end of the table.
  - The processed oil table is saved as a new table in the database, with renamed columns.

- **test_imputer.py:** Performs unit tests on the imputer function in **impute_oil_table.py**.

- **create_data_model.py:** Sets up the rest of the data model:
  - Performed a join operation to add a column for unit sales to the transactions data and created a view with the new table. I ended up not using any transactions data in my dashboard because of the unavailability of detailed information.
  - Truncated the train table to only include dates for which "onpromotion" data is not null; and converted the "onpromotion" values of True/False to Yes/No.
  - Renamed columns for all tables and views.
  - I exported the tables and views to csv's before loading to PBI.

I originally planned on importing only views from DuckDB directly to PBI but was unable to set up this connection, and since I was worked on this in parallel with setting up the data model, my exported csv's come from a combination of view and tables.

After loading the exported csv tables to Power BI, my data model looks like below:

<p align="center">
<img src="images/datamodel1.PNG" alt="Alt text" width="1000"/>
</p>

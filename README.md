# Corporación Favorita
## Analysis of on-promo sales at a large Ecuadorian grocery chain.

Corporación Favorita provided sales data ranging from 2013 to 2017. The data includes information on stores, items, number of units sold, number of items sold on promo, number of transactions at specifc store/date combos (but no transaction data at the itemized level), and oil prices, which have a significant impact on Ecuador's economy. The "On Promotion" data is given as True/False, and I filtered out its null values, which truncated the data set's date range to Apr. 2014 - Aug. 2017.

In this project, I analyzed the data pertaining to items sold on promo. I developed a Power BI dashboard that enables the user to view units sold over time and % of units sold on-promo over time. The dashboard's interactive features allow the user to analyze these trends based on item category, location, different time granularities, and comparing with oil prices.

I chose DuckDB as my database because, with Python, I was able to run SQL queries and code in Pandas to transform the data sets and create my data model for Power BI. There was one processing step where I imputed missing values in the oil prices data table with the average of the nearest available values, and I decided that Pandas was the best tool to perform this.

Data source: https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting/data

## Data Processing Steps and Data Model





<p align="center">
<img src="images/ca-stores-rev.PNG" alt="Alt text" width="600"/>
</p>

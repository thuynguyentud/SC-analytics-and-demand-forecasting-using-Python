# Supply Chain Analytics and Demand Forecasting with Python

This project is my practice with Python, applying statistical models learned during master's program at TU Dresden. It demonstrates a complete data analytics workflow on a real-world supply chain dataset, using **Python** for **ETL (Extract, Transform, Load)**, **Exploratory Data Analysis (EDA)**, and basic **Time Series Forecasting**.

## Dataset
The dataset I used is from Constante, Fabian; Silva, Fernando; Pereira, António (2019), “[DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS](https://data.mendeley.com/datasets/8gx2fvg2k6/5)”, Mendeley Data, V5, doi: 10.17632/8gx2fvg2k6.5. Please cite the dataset and the author if you use this data in your work.

**Why I Chose This Dataset**
I picked this dataset because it feels close to real business problems in logistics and sales. It includes order information, shipping modes, product categories, customer regions, and dates — all useful for understanding supply chain operations from multiple angles. It’s also clean enough to work with, but still complex enough to make the analysis interesting, which is exactly what I needed to improve my data analysis workflow and modeling in Python.

Data Overview:
- Contains over 180,000+ records of customer orders
- Covers multiple countries, products, and customer types
- Includes date-related features for time-based modeling

## Tools & Libraries I used
- **Python** (`pandas`, `numpy`, `matplotlib`, `seaborn`, `pmdarima`, `statsmodels`)
- **VS Code** – main code editor
- **Anaconda** – manages the Python environment, packages, and dependencies
---

## Key Tasks
1. **Data ETL**
This stage includes loading and cleaning the dataset. Irrelevant fields create noise and slow processing.

What was done:
- Dropped irrelevant columns (customer emails, descriptions, GPS data, etc.)
- Parsed order dates and created new time-based features (month, weekday, etc.)
- Removed duplicates and missing values
- Aggregated sales data by **month**

2. **Exploratory Data Analysis (EDA)**
This stage includes exploring and visualizing the data to get insights.

Here are some summary statistics of data features:
---
| Feature               | Count      | Mean     | Min     | 25%     | 50%     | 75%     | Max       | Std Dev  |
|------------------------|------------|----------|---------|---------|---------|---------|-----------|----------|
| Category Id            | 169,138    | 31.80    | 2.00    | 18.00   | 29.00   | 45.00   | 76.00     | 15.76    |
| Order Date             | 169,138    | ~2016-06 | 2015-01 | 2015-09 | 2016-06 | 2017-03 | 2018-01   | –        |
| Order Item Quantity    | 169,138    | 2.17     | 1.00    | 1.00    | 1.00    | 3.00    | 5.00      | 1.47     |
| Sales                  | 169,138    | 202.54   | 9.99    | 119.98  | 199.92  | 299.95  | 1999.99   | 133.55   |
| Order Year             | 169,138    | 2015.97  | 2015    | 2015    | 2016    | 2017    | 2018      | 0.83     |
---

Insights from this:
- Sales are typically between $120 and $300, with a few large outliers up to $1999.
- Orders mainly span 2015 to early 2018, ideal for monthly time series modeling.
- Most orders have 1 to 3 items, averaging around 2.17 items per order.
- Data is evenly distributed across Category IDs, with 2–76 range.

Some visualizations and insights from them:
![Total Sales by Product Category](https://github.com/user-attachments/assets/8dc33105-80bd-42e1-ae4f-507077a7c3bd)

The top 5 product categories generate a significantly higher volume of sales compared to the rest. Most other categories contribute very little to overall revenue, indicating a long tail of low-performing SKUs. This could inform inventory focus, promotional efforts, or bundling strategies.

![Sales by Region](https://github.com/user-attachments/assets/38077d68-591b-4e2b-9d75-b7efecbc0d31)

Western Europe, Central America, and South America are the top three regions by total sales. There's a clear sales imbalance — the bottom regions like Central Asia, Canada, and Southern Africa contribute very little. Potential to expand or market more effectively in underperforming regions, or reduce costs in low-return markets.

![Monthly Sales Trend](https://github.com/user-attachments/assets/a527b8a2-0ab7-4004-8b83-511763f8b7d4)

Sales were relatively stable from 2015 to late 2017, fluctuating around 900k–1.1 M. There is a sharp and unexpected drop starting Nov 2017 — likely due to incomplete or missing data (not actual business decline).
=> Action: Delete the last 3 months of data.

![Trimmed Monthly Sales Trend](https://github.com/user-attachments/assets/d5ebebf5-f112-4456-a18c-d0a80300d59d)
It can be seen that there's some seasonal or operational variability, but no extreme volatility. Without the noisy low months (Nov 2017–Jan 2018), the plot reflects a more realistic and interpretable trend.

3. **Time Series Forecasting**

   - Aggregated monthly sales forecasting  
   - Model comparison: Naive, ARIMA, Seasonal decomposition  
   - KPI-based evaluation (RMSE, MAPE)
---

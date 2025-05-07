# Supply Chain Analytics and Demand Forecasting with Python

This project is my practice with Python, applying statistical models learned during master's program at TU Dresden. It demonstrates a complete data analytics workflow on a real-world supply chain dataset, using **Python** for **ETL (Extract, Transform, Load)**, **Exploratory Data Analysis (EDA)**, and basic **Time Series Forecasting**.

## Dataset
The dataset I used is from Constante, Fabian; Silva, Fernando; Pereira, António (2019), [DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS](https://data.mendeley.com/datasets/8gx2fvg2k6/5). Please cite the dataset and the author if you use this data in your work.

**Why I Chose This Dataset**

I picked this dataset because it feels close to real business problems in logistics and sales. It includes order information, shipping modes, product categories, customer regions, and dates — all useful for understanding supply chain operations from multiple angles. It’s also clean enough to work with, but still complex enough to make the analysis interesting, which is exactly what I needed to improve my data analysis workflow and modeling in Python.

**Data Overview:**

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

**Insights from this:**
- Sales are typically between $120 and $300, with a few large outliers up to $1999.
- Orders mainly span 2015 to early 2018, ideal for monthly time series modeling.
- Most orders have 1 to 3 items, averaging around 2.17 items per order.
- Data is evenly distributed across Category IDs, with 2–76 range.

**Some visualizations and insights from them:**

![Total Sales by Product Category](https://github.com/user-attachments/assets/8dc33105-80bd-42e1-ae4f-507077a7c3bd)

The top 5 product categories generate a significantly higher volume of sales compared to the rest. Most other categories contribute very little to overall revenue, indicating a long tail of low-performing SKUs. This could inform inventory focus, promotional efforts, or bundling strategies.

![Sales by Region](https://github.com/user-attachments/assets/38077d68-591b-4e2b-9d75-b7efecbc0d31)

Western Europe, Central America, and South America are the top three regions by total sales. There's a clear sales imbalance — the bottom regions like Central Asia, Canada, and Southern Africa contribute very little. Potential to expand or market more effectively in underperforming regions, or reduce costs in low-return markets.

![Monthly Sales Trend](https://github.com/user-attachments/assets/a527b8a2-0ab7-4004-8b83-511763f8b7d4)

Sales were relatively stable from 2015 to late 2017, fluctuating around 900k–1.1 M. There is a sharp and unexpected drop starting Nov 2017 — likely due to incomplete or missing data (not actual business decline).
**=> Action: **Removed the last 3 months to avoid distorting the forecast model.

![Trimmed Monthly Sales Trend](https://github.com/user-attachments/assets/d5ebebf5-f112-4456-a18c-d0a80300d59d)
It can be seen that there's some seasonal or operational variability, but no extreme volatility. Without the noisy low months (Nov 2017–Jan 2018), the plot reflects a more realistic and interpretable trend.

3. **Time Series Forecasting**

The goal of this forecast is to predict the next 6-month demand using historical monthly demand. To do this, ARIMA and SARIMA models were used.

** What Are ARIMA and SARIMA?**
- ARIMA (AutoRegressive Integrated Moving Average) is a time series model that looks at patterns in past values and past errors to forecast the future. It also removes trends to make data more predictable.
- SARIMA (Seasonal ARIMA) is just like ARIMA, but it also considers seasonality — repeating patterns over time (like monthly or yearly sales cycles).

I used these 2 models because the dataset includes monthly sales across several years, which fits time series forecasting, and these 2 models are classic and popular in business to use in this case.
However, ARIMA and SARIMA assume the data is stable over time, meaning no big trends or shifting behavior. Therefore, one important step is to conduct a stationarity check using the ADF (Augmented Dickey-Fuller) test. This is a statistical test used in time series analysis to check whether a series is stationary or not.

**Results of ADF Test: **
- ADF Statistic: -0.374
- p-value: 0.914
Interpretation: The p-value is much higher than 0.05, which means the time series is not stationary — it likely has a trend or changing behavior over time. This makes it unsuitable for ARIMA/SARIMA unless they are transformed.

**=> Next steps:** use auto_arima() to detect instationary and apply differencing automatically. Besides, use SARIMA with manual application of differencing.

![Forecasting results ](https://github.com/user-attachments/assets/f69454c4-e41c-4f87-a862-002ee1d1846f)

The plot shows:
- Historical Sales (Blue Line): Sales showed moderate growth with fluctuations, and a noticeable upward trend appeared in late 2017.
- ARIMA Forecast (Red Dashed Line): Continues the rising trend from historical data and predicts higher sales each month/ The confidence interval suggests greater uncertainty in the forecast.
- SARIMA Forecast (Green Line): Captures both trend and seasonal effects (slight dips and rises). The forecast is more conservative and realistic, not overly optimistic. A narrower confidence interval suggests a more stable prediction for short-term planning.

4. **Project Conclusion:**
   
Both models work, but they reflect different assumptions:
- ARIMA fits recent growth aggressively, which can be useful if you expect continued expansion.
- SARIMA is better if seasonality or external cycles (like holidays, campaigns, or market rhythms) matter.
  
🟢 **Recommendation:** Use SARIMA for operational and strategic planning where seasonality matters, and ARIMA as a secondary reference model for trend analysis.

**🧾 Final Thoughts**

This is a hands-on, learning-driven project where I applied forecasting models to understand and predict monthly sales.
I'm actively improving my skills and open to suggestions — feedback is very welcome.

Feel free to open an issue or message me if you have advice or ideas.
More updates, improvements, and model testing will follow soon!

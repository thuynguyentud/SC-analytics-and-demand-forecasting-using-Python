# 📦 Supply Chain Analytics and Demand Forecasting with Python

This project is my practice with Python applying statistical models learned during master program at TU Dresden. It demonstrates a complete data analytics workflow on a real-world supply chain dataset, using **Python** for **ETL (Extract, Transform, Load)**, **Exploratory Data Analysis (EDA)**, and **Time Series Forecasting**.
The dataset I used is from [DataCo Smart Supply Chain for Big Data Analysis](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis). Please cite the dataset and the author if you use this data in your own work.

## 🧠 Why I Chose This Dataset
I picked this dataset from Kaggle because it feels close to real business problems in logistics and sales. It includes order information, shipping modes, product categories, customer regions, and dates — all useful for understanding supply chain operations from multiple angles. It’s also clean enough to work with, but still complex enough to make the analysis interesting — exactly what I needed to improve my data analysis workflow and modeling in Python.

## 🛠️ Tools & Libraries I used
- `pandas`, `numpy` – Data manipulation
- `matplotlib`, `seaborn`, `plotly` – Visualization
- `scikit-learn` – Preprocessing
- `statsmodels`, `pmdarima` – Time series modeling (ARIMA)
---

## 📊 Key Features
1. **Data ETL**  
   - Cleaning and parsing raw CSV files  
   - Handling missing values and date formats  
   - Feature engineering (e.g., demand categories, lead time buckets)
2. **Exploratory Data Analysis (EDA)**  
   - Sales trends by product, region, and channel  
   - Shipping method and cost vs. customer satisfaction  
   - Correlation analysis and outlier detection  
3. **Time Series Forecasting**  
   - Aggregated monthly sales forecasting  
   - Model comparison: Naive, ARIMA, Seasonal decomposition  
   - KPI-based evaluation (RMSE, MAPE)
---

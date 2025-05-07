# %%
#import libraries
import pandas as pd  # For reading, cleaning, and manipulating tabular data
import numpy as np  # For numerical operations and handling arrays
import matplotlib.pyplot as plt # For creating static, animated, and interactive visualizations
import seaborn as sns # For statistical data visualization

# %%
# Time Series & Forecasting
import pmdarima as pm # For time series analysis and forecasting
from statsmodels.tsa.stattools import adfuller # For Augmented Dickey-Fuller test for stationarity

# %%
## Load the data and check the first few rows
df = pd.read_csv('data\\DataCoSupplyChainDataset.csv', encoding='ISO-8859-1')

df.head() #Checking the top 5 rows in the dataset


# %%
#Explore the data
print(df.info())
(df.describe()) # check statistical description of the data in the Dataset

# %%
## DATA PREPROCESSING
# Keep only needed features for analysis for forecasting monthly sales
df = df[[ 
    'Category Id','Category Name', 'Customer Country' , 'Department Name', 'Order Country',  'order date (DateOrders)', 'Order Item Quantity',  'Sales', 'Order Region'
]]

# Remove any duplicate rows
df = df.drop_duplicates()

# rop rows with missing (null) values
df = df.dropna()


# %%
# Convert Order Date to datetime format
df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])

# Rename the column for clarity
df.rename(columns={'order date (DateOrders)': 'Order Date'}, inplace=True) 

#  Create additional time features
df['Order Month'] = df['Order Date'].dt.to_period('M') # Extract month and year from the date
df['Order Year'] = df['Order Date'].dt.year    # Extract year from the date

# %%
# Check data structure after cleaning
print(df.shape) # check the shape of the dataset after cleaning
print(df.head(10)) # check the top 10 rows in the dataset after cleaning
print(df.info())
print(df.describe())

# %%
#Aggregate Monthly Sales
monthly_sales = df.groupby(pd.Grouper(key='Order Date', freq='M'))['Sales'].sum()
monthly_sales = monthly_sales[monthly_sales > 0]  # remove empty months

# %%
# Sales by Category VISUALIZATION
category_sales = df.groupby('Category Name')['Sales'].sum().sort_values()

plt.figure(figsize=(10, 10))
category_sales.plot(kind='barh', color='skyblue')
plt.title('Total Sales by Product Category')
plt.xlabel('Sales')
plt.tight_layout()
plt.show()

# %%
# Sales by Region VISUALIZATION
region_sales = df.groupby('Order Region')['Sales'].sum().sort_values()

plt.figure(figsize=(8, 4))
region_sales.plot(kind='bar', color='lightgreen')
plt.title('Sales by Region')
plt.ylabel('Sales')
plt.tight_layout()
plt.show()

# %%
## VISUALIZATION
# Monthly Sales Trend
plt.figure(figsize=(12, 5))
monthly_sales.plot(marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.grid(True)
plt.tight_layout()
plt.show()

# %%
# The plot shows that from 11.2017 onward, there's a sharp, unnatural drop in sales, which could be due to incomplete data recording, not real business performance
# Solutions: Remove the last 3 months (Nov, Dec 2017, Jan 2018) from the data before forecasting.
monthly_sales_trimmed = monthly_sales.loc[:'2017-10']
print(monthly_sales_trimmed.tail())

# %%
## VISUALIZATION
# Replot the Monthly Sales Trend
plt.figure(figsize=(12, 5))
monthly_sales_trimmed.plot(marker='o')
plt.title('Monthly Sales Trend (Trimmed)')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.grid(True)
plt.tight_layout()
plt.show()

# %%
 #Stationarity Check (ADF Test)
result = adfuller(monthly_sales_trimmed)
print("ADF Statistic:", result[0])
print("p-value:", result[1])
if result[1] < 0.05:
    print(" Time series is stationary")
else:
    print(" Time series is NOT stationary ")

# %%
#Metric	Value
#ADF Statistic	-0.374
#p-value	0.914
#  Time series is NOT stationary 
#It has a trend or changing variance over time
#ARIMA/SARIMA models cannot be applied directly — they assume constant statistical behavior
# ARIMA Model Fitting
#auto_arima() function automatically detects non-stationarity and applies differencing (d and D) as needed.
model = pm.auto_arima(
    monthly_sales_trimmed,
    seasonal=True,
    m=12,
    stepwise=True,
    trace=True,
    suppress_warnings=True
)
# Print summary of fitted model
print(model.summary())

# %%
#Selected Model: ARIMA(2,1,0)(0,0,0)[12]

# ARIMA(2,1,0)
model_arima = pm.ARIMA(order=(2, 1, 0)).fit(monthly_sales_trimmed)
#Forecast Next 6 Months
# ========================
n_periods = 6
forecast, conf_int = model_arima.predict(n_periods=n_periods, return_conf_int=True)

# Create future date index
future_dates = pd.date_range(
    start=monthly_sales_trimmed.index[-1] + pd.offsets.MonthBegin(),
    periods=n_periods,
    freq='M'
)

# Forecast series
forecast_series = pd.Series(forecast, index=future_dates)

# ========================
# 📊 Plot the Forecast
# ========================
plt.figure(figsize=(12, 6))
plt.plot(monthly_sales_trimmed, label='Historical Sales')
plt.plot(forecast_series, label='ARIMA(2,1,0) Forecast', color='red')
plt.fill_between(future_dates, conf_int[:, 0], conf_int[:, 1], color='red', alpha=0.2, label='Confidence Interval')
plt.title("Sales Forecast using ARIMA(2,1,0)")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# %%
# SARIMA(0,0,1)(0,1,0)[12]
model_sarima = pm.ARIMA(order=(0, 0, 1), seasonal_order=(0, 1, 0, 12)).fit(monthly_sales_trimmed)

# ==========================
# 🔮 Forecast Next 6 Months
# ==========================
n_periods = 6
arima_forecast, arima_ci = model_arima.predict(n_periods=n_periods, return_conf_int=True)
sarima_forecast, sarima_ci = model_sarima.predict(n_periods=n_periods, return_conf_int=True)

# Create forecast date range
future_dates = pd.date_range(
    start=monthly_sales_trimmed.index[-1] + pd.offsets.MonthBegin(),
    periods=n_periods, freq='M'
)

# Make series
arima_series = pd.Series(arima_forecast, index=future_dates)
sarima_series = pd.Series(sarima_forecast, index=future_dates)

# ==========================
# 📊 Plot Comparison
# ==========================
plt.figure(figsize=(14, 6))
plt.plot(monthly_sales_trimmed, label='Historical Sales')
plt.plot(arima_series, label='ARIMA(2,1,0) Forecast', linestyle='--', color='red')
plt.plot(sarima_series, label='SARIMA(0,0,1)(0,1,0)[12] Forecast', linestyle='-', color='green')
plt.fill_between(future_dates, arima_ci[:, 0], arima_ci[:, 1], color='red', alpha=0.2)
plt.fill_between(future_dates, sarima_ci[:, 0], sarima_ci[:, 1], color='green', alpha=0.2)
plt.title("📊 Sales Forecast: ARIMA vs SARIMA")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



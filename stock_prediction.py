import yfinance as yf
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime

# Download historical data for AAPL stock
today = datetime.today().strftime('%Y-%m-%d')
df = yf.download('AAPL', start='2010-01-01', end=today)

# Extract the closing prices from the dataframe
stock_prices = df['Close'].values

# Generate chaotic data
def generate_chaos(x0, r, n):
    x = np.zeros(n)
    x[0] = x0
    for i in range(1, n):
        x[i] = r * x[i-1] * (1 - x[i-1])
    return x

# Generate stock price data
def generate_stock_prices(x0, r, n, actual_prices):
    chaos_data = generate_chaos(x0, r, n)
    min_price = min(actual_prices)
    max_price = max(actual_prices)
    stock_prices = min_price + (max_price - min_price) * chaos_data
    return stock_prices

# Calculate Average True Range (ATR)
def calculate_atr(stock_prices, window=14):
    high_prices = df['High'].values
    low_prices = df['Low'].values
    tr = np.maximum(high_prices - low_prices, np.abs(high_prices - np.roll(stock_prices, 1)))
    atr = np.mean(tr[:window])
    return atr

# Perform time series forecasting using ARIMA model
def forecast_stock_prices(stock_prices, order=(1, 1, 1)):
    model = ARIMA(stock_prices, order=order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=5)  # Forecast for next 5 days
    return forecast

# Perform analysis and provide trading instructions
def analyze_stock(stock_prices, forecast, atr_threshold):
    current_price = stock_prices[-1]
    future_prices = forecast

    # Calculate Average True Range (ATR) for recent data
    atr = calculate_atr(stock_prices)

    if atr > atr_threshold:
        return 'Hold'  # No clear prediction when ATR exceeds the threshold

    # Check for significant changes (punctuated equilibrium)
    previous_close = stock_prices[-2]
    price_change_percent = (current_price - previous_close) / previous_close * 100

    if abs(price_change_percent) >= 1.5:
        if price_change_percent > 0:
            return 'Buy'
        else:
            return 'Sell'

    # Check ARIMA forecast for trading decision
    future_avg_price = np.mean(future_prices)
    if future_avg_price > stock_prices[-1]:  # Compare ARIMA forecast with current stock price
        return 'Buy'
    elif future_avg_price < stock_prices[-1]:  # Compare ARIMA forecast with current stock price
        return 'Sell'
    else:
        return 'Hold'

# Parameters for chaos and stock price generation
x0 = 0.5  # Initial condition
r = 3.9  # Control parameter
n = len(stock_prices) + 1  # Number of data points

# Generate chaotic stock price data
chaotic_prices = generate_stock_prices(x0, r, n, stock_prices)

# Perform time series forecasting
forecast = forecast_stock_prices(stock_prices)

# Set ATR threshold for volatility detection
atr_threshold = 5.0  # Adjust this threshold as needed based on historical data analysis

# Analyze stock prices and provide trading instructions
trading_instruction = analyze_stock(stock_prices, forecast, atr_threshold)

# Get the current date and tomorrow's date
current_date = datetime.today().strftime('%Y-%m-%d')
tomorrow_date = (datetime.today() + pd.DateOffset(days=1)).strftime('%Y-%m-%d')

# Print the results
print('Historical Stock Prices:')
print(df)

print('\nChaotic Stock Prices:')
print(chaotic_prices)

print('\nARIMA Forecast for Next 5 Days:')
print(forecast)

# Get the chaotic stock price for tomorrow
chaotic_price_tomorrow = chaotic_prices[-1]

# Get the ARIMA forecast for tomorrow
arima_forecast_tomorrow = forecast[0]

# Print trading instruction for tomorrow
if trading_instruction == 'Buy':
    print(f'\n{tomorrow_date} - Trading Instruction: {trading_instruction}')
elif trading_instruction == 'Sell':
    print(f'\n{tomorrow_date} - Trading Instruction: {trading_instruction}')
else:
    print(f'\n{tomorrow_date} - Trading Instruction: {trading_instruction}')

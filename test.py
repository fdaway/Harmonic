import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the CSV file
data = pd.read_csv('EURAUD-4h-2020-2023-Jul-1 - EURAUD_H4_202001020000_202306302000.csv', parse_dates=[['Date', 'Time']], dayfirst=True)

# Set the Date_Time column as the index
data.set_index('Date_Time', inplace=True)

# Calculate short-term (e.g., 2 periods) and long-term (e.g., 5 periods) moving averages
short_window = 270
long_window = 420

data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
data['Long_MA'] = data['Close'].rolling(window=long_window).mean()

# Generate buy/sell signals based on crossover using boolean mask
data['Signal'] = 0
data['Signal'].loc[data['Short_MA'].shift() > data['Long_MA'].shift()] = 1

# Calculate position based on signal
data['Position'] = data['Signal'].diff()

# Plot the price data and moving averages
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label='Close Price')
plt.plot(data.index, data['Short_MA'], label=f'Short {short_window} periods MA')
plt.plot(data.index, data['Long_MA'], label=f'Long {long_window} periods MA')

# Plot buy signals (green) and sell signals (red)
buy_signals = data[data['Position'] == 1]['Short_MA']
sell_signals = data[data['Position'] == -1]['Short_MA']
plt.plot(buy_signals.index, buy_signals, '^', markersize=10, color='g', label='Buy Signal')
plt.plot(sell_signals.index, sell_signals, 'v', markersize=10, color='r', label='Sell Signal')

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('MA Crossover Strategy')
plt.legend()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Read the data from 'test.csv'
data = pd.read_csv('data/EURAUD_H4_2020-01-02-C.csv')
df = pd.DataFrame(data)

# Convert 'Date' and 'Time' columns to datetime format
df['Date'] = pd.to_datetime(df['Date'])
df['Time'] = pd.to_datetime(df['Time'])

# Combine 'Date' and 'Time' columns into a single DateTime column
df['DateTime'] = df['Date'] + pd.to_timedelta(df['Time'].dt.hour, unit='h')
df.set_index('DateTime', inplace=True)

# Calculate the 3-period moving average for the 'Close' column and add it as a new column (renamed to 'MA')
df['MA'] = df['Close'].rolling(window=7).mean()

# Replace NaN values in 'MA' column with the average between 'Open' and 'Close'
df['MA'].fillna((df['Open'] + df['Close']) / 2, inplace=True)

# Generate buy (1) and sell (-1) signals based on Close and MA comparison
df['Signal'] = 0  # Initialize the 'Signal' column with 0

# Set buy signal (1) when Close is above MA
df.loc[df['Close'] > df['MA'], 'Signal'] = 1

# Set sell signal (-1) when Close is below MA
df.loc[df['Close'] < df['MA'], 'Signal'] = -1

# Calculate returns based on the signals
df['Returns'] = 0.0  # Initialize the 'Returns' column with 0.0

for i in range(1, len(df)):
    if df['Signal'][i - 1] == 1:  # Buy Signal
        df.loc[df.index[i], 'Returns'] = df['Close'][i] - df['Close'][i - 1]
    elif df['Signal'][i - 1] == -1:  # Sell Signal
        df.loc[df.index[i], 'Returns'] = df['Close'][i - 1] - df['Close'][i]

# Calculate cumulative returns and rename the column
df['cumReturns'] = df['Returns'].cumsum()

# Multiply cumulative returns by a factor (3 in this case)
factor = 3
df['cumReturns'] *= factor

# Print the updated DataFrame with signals, returns, and adjusted cumulative returns
print(df)
cumReturns = df['cumReturns']
cumReturns_max = cumReturns.cummax()
drawdown = cumReturns - cumReturns_max
max_drawdown = drawdown.min()

print("Maximum Drawdown:", max_drawdown)
# Plot the original 'Close' data, the MA, and the buy/sell signals with adjusted cumulative returns
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Close'], label='Close')
plt.plot(df.index, df['MA'], label='MA')
plt.scatter(df.index[df['Signal'] == 1], df[df['Signal'] == 1]['Close'], marker='^', color='g', label='Buy Signal')
plt.scatter(df.index[df['Signal'] == -1], df[df['Signal'] == -1]['Close'], marker='v', color='r', label='Sell Signal')
plt.plot(df.index, df['cumReturns'], label=f'Adjusted Cumulative Returns (x{factor})', linestyle='--')
plt.xlabel('Date and Time')
plt.ylabel('Value')
plt.title('Close Price vs MA with Buy/Sell Signals and Adjusted Cumulative Returns')
plt.legend()
plt.show()


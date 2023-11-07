import pandas as pd

data = pd.read_csv('data/EURAUD_H4_2020-01-02_2023-06-30-C.csv')

ma_window = 7
spread = 0.00012

data['Signal'] = 0 
data['Returns'] = 0.0

data['MA'] = data['Close'].rolling(window=ma_window).mean()
data['MA'].fillna((data['Open'] + data['Close']) / 2, inplace=True)

data.loc[data['Close'] >= data['MA'], 'Signal'] = 1
data.loc[data['Close'] < data['MA'], 'Signal'] = -1

for i in range(1, len(data)):
    if data['Signal'][i - 1] == 1:  
        data.loc[data.index[i], 'Returns'] = data['Close'][i] - (data['Close'][i - 1] + spread)
    elif data['Signal'][i - 1] == -1:  
        data.loc[data.index[i], 'Returns'] = (data['Close'][i - 1] - spread) - data['Close'][i]

data['CumReturns'] = data['Returns'].cumsum()
trades = sum(abs(data['Signal'][i] - data['Signal'][i - 1]) == 2 for i in range(1, len(data)))
net_returns = data['CumReturns'].iloc[-1] - (spread * trades)

print("Net Returns with Commissions:", net_returns)
print("Total Trades:", trades)

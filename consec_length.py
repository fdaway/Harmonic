import pandas as pd
import matplotlib.pyplot as plt

# Read the data and create the DataFrame
data = pd.read_csv('data/EURAUD-4h-2020-2023-Jul-1 - EURAUD_H4_202001020000_202306302000.csv')
df = pd.DataFrame(data)

print(df)
# Calculate 'Change', 'Direction', 'Consec', and 'Counter' columns
df['Change'] = df['Close'].diff().fillna(0) / df['Close'] * 100
df['Direction'] = df['Change'].apply(lambda x: 'Up' if x >= 0 else 'Down')
df['Consec'] = df['Direction'].eq(df['Direction'].shift(fill_value=df['Direction'].iloc[0])).apply(lambda x: '+' if x else '-')
df['Counter'] = df.groupby((df['Consec'] != df['Consec'].shift()).cumsum()).cumcount()

# Extract subsets for each 'Counter' value
consecs_0 = df[df['Counter'] == 0]
consecs_1 = df[df['Counter'] == 1]
consecs_2 = df[df['Counter'] == 2]
consecs_3 = df[df['Counter'] == 3]
consecs_4 = df[df['Counter'] == 4]
consecs_5 = df[df['Counter'] == 5]
consecs_6 = df[df['Counter'] == 6]
consecs_7 = df[df['Counter'] == 7]

print(df)
# Print the lengths of each 'consecs_x' subset
print("Consec 0 length:", len(consecs_0))
print("Consec 1 length:", len(consecs_1))
print("Consec 2 length:", len(consecs_2) * 2)
print("Consec 3 length:", len(consecs_3) * 4)
print("Consec 4 length:", len(consecs_4) * 6)
print("Consec 5 length:", len(consecs_5) * 8)
print("Consec 6 length:", len(consecs_6) * 16)
print("Consec 7 length:", len(consecs_7) * 32)
 

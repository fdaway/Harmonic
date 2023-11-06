import pandas as pd

data = {
    'Value': [5642, 2811, 1400, 714, 358, 183, 89, 49, 22]
}

df = pd.DataFrame(data)

# Calculate the expected next value (50% of the current value)
df['Expected_Next_Value'] = df['Value'].shift() * 0.5

# Calculate the deviation from the expected value in percentages
df['Deviation_from_Expected'] = ((df['Value'] / df['Expected_Next_Value']) - 1) * 100

print(df)
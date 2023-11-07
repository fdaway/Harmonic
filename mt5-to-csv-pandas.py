import os
import pandas as pd

# Define the folder name
folder_name = 'data'

# Check if the folder exists, if not, create it
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Read the CSV file from the 'data' folder into a pandas DataFrame
filename = 'EURAUD_H4_202001020000_202306302000.csv'
input_file_path = os.path.join(folder_name, filename)
df = pd.read_csv(input_file_path, sep='\t')

# Remove brackets from column names, capitalize the first letter, and make the rest lowercase
df.columns = df.columns.str.strip('<').str.strip('>').str.title()

# Drop the 'Vol' column from the DataFrame
df = df.drop(columns=['Vol','Tickvol', 'Spread'])

# Convert 'Date' and 'Time' columns to datetime format
df['Date'] = pd.to_datetime(df['Date'])
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time

# Derive the output filename using the specified format
currency_pair = filename.split('_')[0]
timeframe = filename.split('_')[1]
start_date = filename.split('_')[2][:8]
end_date = filename.split('_')[3][:8]
output_filename = f'{currency_pair}_{timeframe}_{start_date[:4]}-{start_date[4:6]}-{start_date[6:8]}_{end_date[:4]}-{end_date[4:6]}-{end_date[6:8]}-C.csv'

# Save the cleaned DataFrame to the 'data' folder with the derived output filename
output_file_path = os.path.join(folder_name, output_filename)
df.to_csv(output_file_path, index=False)

print(f"The cleaned data has been saved to {output_file_path}")

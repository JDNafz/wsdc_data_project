from datetime import date

import pandas as pd # type: ignore
import glob

# Get all CSV files in a folder (modify the path as needed)
files = glob.glob(r"C:\Users\nafzi\Documents\projects\wsdc_data_project\data_scraped\set1_3_3_2025\*.csv")

# Read and combine CSV files
dfs = []
for file in files:
    df = pd.read_csv(file)
    dfs.append(df)

# Concatenate all dataframes
combined_df = pd.concat(dfs, ignore_index=True).drop_duplicates()

# Save to a new CSV file
today = str(date.today())
outputPath = r"C:\\Users\\nafzi\\Documents\\projects\\wsdc_data_project\\data_scraped\\"
combined_df.to_csv(outputPath + 'all_westies_' + today + ".csv", index=False)
print("Combined CSV file saved successfully!")
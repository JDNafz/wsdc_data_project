import pandas as pd # type: ignore

# Read the CSV file
file_path = r'data_scraped\Point_DF_13758-13759_2025-03-02.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
print(data.head())

# Sum up the competition points from all the events
total_points = data['points'].sum()
# Sum up the competition points from all the events, sorted by level
total_points_by_level = data.groupby('level')['points'].sum().sort_values(ascending=False)
print(total_points_by_level)
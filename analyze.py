# Run py summarize.py to see the summary of the data

import pandas as pd # type: ignore
# import json
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file
file_path = r'C:\Users\nafzi\Documents\projects\wsdc_data_project\data_scraped\points_df_0-2001_2025-03-02.csv'
just_JD = r'C:\Users\nafzi\Documents\projects\wsdc_data_project\data_scraped\JD_example_2025-03-02.csv'

data = pd.read_csv(file_path)
# data = pd.read_csv(just_JD)

DataFrameColumns=[
    "wsdc_id", # integer
    "level_points", #total points at level "NOV_123" NOV separated by _ then total number of points in that division between both roles
    "allowed_level", #highest level allowed
    "required_level", #correlations between event level and required?
    "event_level", #level of the event
    "event_name",
    "event_location",
    "event_date",
    "points", #points earned
    "result", #placement 1st, 2nd, 3rd, etc then F for Finaled
    "role", #leader or follower
    "first_name",
    "last_name",
]

# print("\n Data Info:\n",data.info())
# print("\n Data is Null:\n",data.isnull().sum())
# print(data.describe())

person_metrics = data.groupby('wsdc_id').agg(
    total_points=('points', 'sum'),  # Total points earned
    num_competitions=('wsdc_id', 'count'),  # Number of competitions
    avg_points_per_competition=('points', 'mean'),  # Average points per competition
    highest_placement=('result', 'min'),  # Best placement (1 is the best)
    num_wins=('result', lambda x: (x == 1).sum()),  # Number of 1st place finishes
    most_frequent_role=('role', lambda x: x.mode()[0]),  # Most frequent role (leader/follower)
    earliest_competition_date=('event_date', 'min'),  # First competition date
    latest_competition_date=('event_date', 'max')  # Last competition date
).reset_index()

# Display the first few rows of the metrics
# print(person_metrics)


# Step 1: Filter people who have competed at CHMP, INV, or PRO levels
high_level_competitors = data[data['event_level'].isin(['CHMP', 'INV', 'PRO'])]

# Get the unique wsdc_id of these competitors
high_level_ids = high_level_competitors['wsdc_id'].unique()

# Step 2: Filter the dataset to include only these competitors
high_level_data = data[data['wsdc_id'].isin(high_level_ids)]

# Step 3: Count the number of Novice (NOV) competitions for each person
adv_counts = high_level_data[high_level_data['event_level'] == 'ADV'].groupby('wsdc_id').size().reset_index(name='adv_count')

# Step 4: Merge with the high_level_data to include all competitors (even those with 0 NOV competitions)
adv_counts = pd.merge(pd.DataFrame({'wsdc_id': high_level_ids}), adv_counts, on='wsdc_id', how='left').fillna(0)

# Step 5: Calculate the average number of Novice competitions
average_adv_count = adv_counts['adv_count'].mean()

print(f"Average number of Advanced competitions for people who competed at CHMP, INV, or PRO levels: {average_adv_count:.2f}")
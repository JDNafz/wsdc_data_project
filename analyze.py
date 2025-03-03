# Run py summarize.py to see the summary of the data

import pandas as pd # type: ignore
import json

# Read the CSV file
file_path = r'C:\Users\nafzi\Documents\projects\wsdc_data_project\data_scraped\points_df_0-2001_2025-03-02.csv'
just_JD = r'C:\Users\nafzi\Documents\projects\wsdc_data_project\data_scraped\JD_example_2025-03-03.csv'

# data = pd.read_csv(file_path)
data = pd.read_csv(just_JD)

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
print(data.describe())

# Come back to this later, I need to make sure to 
# divide lead and follow points before getting to 
# deep into processing the data to format it.

# import numpy as np
import pandas as pd


# point_df = pd.DataFrame(columns = ['wsdc_id', 'level_points', 'allowed_level', 'required_level', \
#                                    'event_level', 'event_name', 'event_location', 'event_date', \
#                                    'points', 'result', 'role', 'first_name', 'last_name'])

file_path = 'DF1.csv'

df = pd.read_csv(file_path)

# print(df.to_string())

# df.head()
# df.tail()

id = df['wsdc_id'].to_string
role = df['role'].to_string()
lvl = df['event_level'].to_string()
points = df['points'].to_string()
name = df['first_name'].to_string()
# print("BREAK")

dancers = {}
if id not in dancers:
    dancers.update({id: name})
    print('new dancer', dancers[id])
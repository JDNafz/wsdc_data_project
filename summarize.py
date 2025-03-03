import pandas as pd # type: ignore
import json

# Read the CSV file
file_path = r'C:\Users\nafzi\Documents\projects\wsdc_data_project\data_scraped\JD_example_2025-03-02.csv'

data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
# print(data.head())

def getLvl(level):
    if level == 'JR':
        return 1
    elif level == 'NEW':
        return 2
    elif level == 'NOV':
        return 3
    elif level == 'INT':
        return 4
    elif level == 'ADV':
        return 5
    elif level == 'ALS':
        return 6
    elif level == 'CHAMP' or level == 'PRO' or level == 'ALS+':
        return 7
    else:
        return 0
def getLvlStr(level):
    if level == 1:
        return 'JR'
    elif level == 2:
        return 'NEW'
    elif level == 3:
        return 'NOV'
    elif level == 4:
        return 'INT'
    elif level == 5:
        return 'ADV'
    elif level == 6:
        return 'ALS'
    elif level == 7:
        return 'CHAMP'
    else:
        return 'ERR'

current_dancer = {
    'wsdc_id' : None,
    'first_name' : None,
    'last_name' : None,
    'allowed_leader_level' : 0,
    'allowed_follower_level' : 0,
    'follower_points' : [0,0,0,0,0,0,0,0], # 0 ERR, 1 JR, 2 NEW, 3 NOV, 4 INT, 5 ADV, 6 ALS, 7 CHAMP
    'leader_points' : [0,0,0,0,0,0,0,0], 
    'division_points' : [0,0,0,0,0,0,0,0],
    'total_points' : 0,
}


# Sum up the competition points from all the events
for index, row in data.iterrows():
    # if index == 0:
    #     print("i:",index, "row:", row, "END INIT PRINT \n\n")
    #if it's a new dancer, reset the current dancer
    event_level = getLvl(row['event_level'])
    event_points = row['points']
    event_role = row['role']

    follower_points = current_dancer['follower_points']
    leader_points = current_dancer['leader_points']
    division_points = current_dancer['division_points']

    rowID = row['wsdc_id']
    currentDancerID = current_dancer['wsdc_id']
    if rowID != currentDancerID:
        #print the current dancer
        # print(current_dancer)
        #reset the current dancer
        current_dancer = {
            'wsdc_id' : row['wsdc_id'],
            'first_name' : row['first_name'],
            'last_name' : row['last_name'],
            'allowed_leader_level' : 0,
            'allowed_follower_level' : 0,
            'follower_points' : [0,0,0,0,0,0,0,0],
            'leader_points' : [0,0,0,0,0,0,0,0], 
            'division_points' : [0,0,0,0,0,0,0,0],
            'total_points' : 0,
        }
    else:        
        # if leader add lead points
        if row['role'] == 'leader':
            for i in range(len(current_dancer['leader_points']) -1,-1,-1):
                # if level 5 event = index of range
                if event_level == i:
                    # add the points to the current dancer
                    current_dancer['leader_points'][i] += event_points
                    current_dancer['division_points'][i] += event_points
                    current_dancer['total_points'] += event_points
                    if getLvl(current_dancer['allowed_leader_level']) < event_level:
                        current_dancer['allowed_leader_level'] = getLvlStr(event_level)

        # is follower add follow points
        else:
            for i in range(len(current_dancer['follower_points']) -1,-1,-1):
                # if level 5 event = index of range
                if event_level == i:
                    # add the points to the current dancer
                    current_dancer['follower_points'][i] += event_points
                    current_dancer['division_points'][i] += event_points
                    current_dancer['total_points'] += event_points
                    if getLvl(current_dancer['allowed_follower_level']) < event_level:
                        current_dancer['allowed_follower_level'] = getLvlStr(event_level)

allowed_leader_level = getLvl(current_dancer['allowed_leader_level'])
allowed_follower_level = getLvl(current_dancer['allowed_follower_level'])

leadLvlStr = getLvlStr(allowed_leader_level)
followLvlStr = getLvlStr(allowed_follower_level)
lDivPoints = current_dancer['leader_points'][allowed_leader_level]
fDivPoints = current_dancer['follower_points'][allowed_follower_level]


print("\n", current_dancer['first_name'], " ", current_dancer['last_name'])
print(leadLvlStr, "Leader with ", lDivPoints)
print(followLvlStr,"Follower with ", fDivPoints, "\n")



DataFrameColumns=[
    "wsdc_id",
    "level_points",
    "allowed_level",
    "required_level",
    "event_level",
    "event_name",
    "event_location",
    "event_date",
    "points",
    "result",
    "role",
    "first_name",
    "last_name",
]
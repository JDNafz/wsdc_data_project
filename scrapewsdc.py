import pandas as pd
import openpyxl, requests, pprint, time
from datetime import date
import simplejson as json




API_url = 'https://points.worldsdc.com/lookup/find'

point_df = pd.DataFrame(columns = ['wsdc_id', 'level_points', 'allowed_level', 'required_level', \
                                   'event_level', 'event_name', 'event_location', 'event_date', \
                                   'points', 'result', 'role', 'first_name', 'last_name'])
today = date.today() # the collection date will be appended to the excel file so I know when I ran it



# Pick the start and end numbers. Note that it's best to do 5-10k numbers at a time (takes ~1-2hr to run)
#    instead of doing the whole thing at once (which takes 4-6 hours)
start = 13758
end = 13760

# start = 420 #test case for a dance ID that doesn't exist 
# end = 421
# up to 21606 as of 2023-04-01

# print(point_df) # print the initialized empty dataframe




# Loop to go through every WSDC number
for wsdc_id in range(start, end):
    try:
        response = requests.post(API_url, {'q': wsdc_id}).json()
        
        # print(response)

        # only cases with valid WSDC IDs containing WCS placements
        print(response)
        if len(response) > 2 and response['placements'] != [] and 'West Coast Swing' in response['placements'].keys():
            # print('Westie confirmed.')
            westie = response['placements']['West Coast Swing']
            
            #Extract dancer's level information and name
            allowed_level = response['level']['allowed']
            required_level = response['level']['required']
            first_name = response['dancer']['first_name']
            last_name = response['dancer']['last_name']
            
            #Extract information on a per level and per event basis
            for event_level in westie:
                # print(event_level + " of " + str(len(westie)))
                tot_points = westie[event_level]['total_points']
                # print(tot_points, event_level)
                eventList = westie[event_level]['competitions']

                for i in range(len(eventList)):
                    #print(str(i) + " of " + str(len(eventList)))
                    event_name = eventList[i]['event']['name']
                    event_date = eventList[i]['event']['date']
                    event_location = eventList[i]['event']['location']
                    if eventList[i]['role'] == 'leader':
                        leader_points = eventList[i]['points']
                    else:
                        follower_points = eventList[i]['points']
                    result = eventList[i]['result']
                    role = eventList[i]['role']
                    #print(role)

                    obs = { 'wsdc_id': wsdc_id, \
                            'level_points': str(event_level)+'_'+str(tot_points), \
                            'allowed_level': allowed_level, \
                            'required_level': required_level, \
                            'event_level': event_level, \
                            'event_name': event_name, \
                            'event_location': event_location, \
                            'event_date': event_date, \
                            'leader_points': leader_points,\
                            'follower_points': follower_points,\
                            'result': result, 'role': role, \
                            'first_name': first_name, 'last_name': last_name}
                    
                    point_df_new_row = pd.DataFrame(obs, index = [0])
                    point_df = pd.concat([point_df, point_df_new_row], ignore_index = True)   


            if wsdc_id % 2000 == 0:
                point_df.to_csv('C:\\Users\\nafzi\\Desktop\\WSDCdata\\Point_DF_'+str(today)+'updating.csv')
            
        print('Dancer #'+str(wsdc_id)+' completed.')
        # sleep for 0.5 seconds on each for loop to let WSDC website rest
        time.sleep(0.5)
                    
                    #print('Westie #'+str(wsdc_id)+' got '+str(points)+' points as a '+role+' in '+event_date \
                    #     +'. They are level '+allowed_level+'.')
        #else:
               #print('No such westie with #' + str(wsdc_id) + ' exists.')
    except ValueError as IndexError:
        continue
print('That\'s all the westies!')






# Export dataframe to a csv file with the path shown
# point_df.to_csv('C:\\Users\\nafzi\\Desktop\\WSDCdata\\Point_DF_'+str(start)+'-'+str(end)+'_'+str(today)+'.csv')



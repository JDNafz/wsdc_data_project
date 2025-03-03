#To run this file and scrape data, 
# 1. Edit line 170 to change the range of WSDC IDs to scrape
# 2. Run the following command in the terminal:
# py scrapewsdc.py
# 3/2/2025 Python 3.11.0



# Standard library imports
from datetime import date
import time

# Third-party imports
import pandas as pd # type: ignore
import requests # type: ignore # openpyxl and pprint removed from list
import simplejson as json # type: ignore

API_url = "https://points.worldsdc.com/lookup/find"

point_df = pd.DataFrame(
    columns=[
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
)
today = (
    date.today()
)  # the collection date will be appended to the excel file so I know when I ran it

def format_time(time):
    # Convert to hours, minutes, and seconds
    hours, remainder = divmod(int(time), 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format as "HH:MM:SS"
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"

    # print(f"Elapsed time: {formatted_time}")
    return formatted_time
    
# print(point_df) # print the initialized empty dataframe
def scrape(start, end, export=True):
    global point_df
    start_time = time.time()
    print_counter= 0
    # Loop to go through every WSDC number
    for wsdc_id in range(start, end):
        try:
            response = requests.post(API_url, {"q": wsdc_id}).json()
            # print(response)
            # only cases with valid WSDC IDs containing WCS placements
            if (
                len(response) > 2  # more than two dancers
                and response["placements"] != []  # placements are not empty
                and "West Coast Swing"
                in response[
                    "placements"
                ].keys()  # has WCS placements rather than non-WCS placements
            ):
                # westie is an http response object returned by the API when searching for a WSDC ID
                westie = response["placements"]["West Coast Swing"]

                # Extract dancer's level information and name
                allowed_level = response["level"]["allowed"]
                required_level = response["level"]["required"]
                first_name = response["dancer"]["first_name"]
                last_name = response["dancer"]["last_name"]

                # Extract information on a per level and per event basis
                for event_level in westie: # event_level is ADV, INT, NOV, etc.
                    tot_points = westie[event_level]["total_points"] #tot_points is the total points for that level                    
                    eventList = westie[event_level]["competitions"] #all the events attended at that level

                    for i in range(len(eventList)):
                        # print(str(i) + " of " + str(len(eventList)))
                        event_name = eventList[i]["event"]["name"]
                        event_date = eventList[i]["event"]["date"]
                        event_location = eventList[i]["event"]["location"]
                        points = eventList[i]["points"]
                        role = eventList[i]["role"]
                        points = eventList[i]["points"]
                        result = eventList[i]["result"]

                        obs = {
                            "wsdc_id": wsdc_id,
                            "level_points": str(event_level) + "_" + str(tot_points),
                            "allowed_level": allowed_level,
                            "required_level": required_level,
                            "event_level": event_level,
                            "event_name": event_name,
                            "event_location": event_location,
                            "event_date": event_date,
                            "points": points,
                            "result": result,
                            "role": role,
                            "first_name": first_name,
                            "last_name": last_name,
                        }

                        point_df_new_row = pd.DataFrame(obs, index=[0])
                        point_df = pd.concat(
                            [point_df, point_df_new_row], ignore_index=True
                        )
                if wsdc_id % 5000 == 0:
                    point_df.to_csv(
                        "C:\\Users\\nafzi\\Documents\\projects\\wsdc_data_project\\data_scraped\\points_df_"
                        + str(today)
                        + "_2k_done_still_scraping.csv"
                    )
                #if current iteration % 50 ... then
                startMod50 = start - start % 63 # about once per minute?
                currentIteration = wsdc_id - startMod50
                if currentIteration % 1000 == 0:
                    midPoint_time = time.time()
                    midelapsed_time = midPoint_time - start_time
                    print_counter += 1
                    print("\n",str(currentIteration), " completed, Westie #" + str(wsdc_id) + " completed. Counter:", print_counter)
                    print("Elapsed time: ", format_time(midelapsed_time))
                    
                    
            # print('Dancer #'+str(wsdc_id)+' completed.')
            # sleep for 0.5 seconds on each for loop to let WSDC website rest
            time.sleep(0.5)
            # print('Westie #'+str(wsdc_id)+' got '+str(points)+' points as a '+role+' in '+event_date \
            #     +'. They are level '+allowed_level+'.')
            # else:
            # print('No such westie with #' + str(wsdc_id) + ' exists.')

            if export:
                # this should be removed after testing. It's just to test the JD example
                if start == 13758 and end == 13759:
                    point_df.to_csv(
                        "C:\\Users\\nafzi\\Documents\\projects\\wsdc_data_project\\data_scraped\\JD_example"
                        + "_"
                        + str(today)
                        + ".csv"
                    )
                else:
                    # in the file name df stands for dataframe (which is the csv file)
                    point_df.to_csv(
                        "C:\\Users\\nafzi\\Documents\\projects\\wsdc_data_project\\data_scraped\\points_df_"
                        + str(start)
                        + "-"
                        + str(end)
                        + "_"
                        + str(today)
                        + ".csv"
                    )
        except ValueError as IndexError:
            continue
    end_time = time.time()
    total_time = end_time - start_time
    
    print('Completed Westie #',wsdc_id,'\nThat\'s all the westies!')
    print("Total elapsed time: ", format_time(total_time))






# Note that it's best to do 5-10k numbers at a time (takes ~1-2hr to run) 
#     instead of doing the whole thing at once (which takes 4-6 hours)
#   ~2023

# 3/2/2025 1.06/second for 2000 IDs > 33898.11 per hour



# scrape(0, 8500, True)      # Collect and compile a large data set - 0    to 8.5k
# scrape(8500, 17000, True)  # Collect and compile a large data set - 8.5k to 17k
# scrape(17000, 25500, True) # Collect and compile a large data set - 17k  to 25.5k (end)



# Test cases: 
# scrape(13758, 13759, False) # JD's points 
# scrape(420, 421, False) # ID doesn't exist

# max ID number is 25154 (25,154) as of 3/2/2025

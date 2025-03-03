#To run this file and scrape data, 
# 1. Edit line 148 to change the range of WSDC IDs to scrape
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


# print(point_df) # print the initialized empty dataframe
def scrape(start, end, export=True):
    global point_df
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
                if wsdc_id % 2000 == 0:
                    point_df.to_csv(
                        "C:\\Users\\nafzi\\Documents\\projects\\wsdc_data_project\\data_scraped\\points_df_"
                        + str(today)
                        + "2k_done_still_scraping.csv"
                    )

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
    print('That\'s all the westies!')





# Note that it's best to do 5-10k numbers at a time (takes ~1-2hr to run)
#     instead of doing the whole thing at once (which takes 4-6 hours)

# scrape(100,200, True) # Collect and compile a large data set

# Test cases: 
# scrape(13758, 13759, False) # JD's points 
# scrape(420, 421, False) # ID doesn't exist

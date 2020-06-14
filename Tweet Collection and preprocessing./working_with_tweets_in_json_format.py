

import os
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import geopandas as gpd
from pygeocoder import Geocoder
import reverse_geocoder as rg
import pprint


# The JSON file has thousands of JSON objects in it, so we need to first open the file,
# loop through each line, and use the json.loads() function to extract each object, which is one Tweet.
sample = 'randomsample5_round4'
tweets = []
with open(sample+".jsonl") as f:
    for line in f:
        tweets.append(json.loads(line))

# How many tweets do we have in this JSON file
len(tweets)

# What the available data looks like for one tweet
tweets[1]

# How many variables are in this tweet in JSON form
w = str(tweets[1])
words = {}
for ws in w:
    if ws not in words:
        words[ws] = 1
    else:
        words[ws] += 1
print("There are {} keys (including nested keys) in this JSON object".format(words[':']))

"""#### Note: The number of keys changes with each text because some Twitter profiles have more information, such as a background image, whether or not the tweet was in reply to another tweet, etc.

### Look at Text from Tweets
"""

[print(tweets[i]['full_text'] +'\n') for i in range(5)]

# If a Tweet was retweeted, the text may be shortened. For example, in this tweet below the 'full text'
# is actually cut short, but in the retweeted status we can see the full text.
print(tweets[27]['full_text']), tweets[27]['retweeted_status']['full_text']


# Hand-code the locations of interest in each state (collection of cities with unique names)
locationsofinterest = ['seattle', 'spokane', 'tacoma', 'bellingham', 'tri cities', 'yakima', 'olympia',
                       'wa', 'washington state', 'seattle, wa', 'spokane, wa', 'tacoma, wa', 'bellingham, wa',
                       'tri cities, wa', 'yakima, wa', 'olympia, wa', 'seattle, washington', 'spokane, washington',
                       'tacoma, washington', 'bellingham, washington', 'tri cities, washington', 'yakima, washington',
                       'olympia, washington',
                       'miami', 'tampa', 'tampa bay', 'jacksonville', 'orlando', 'fl', 'florida',
                       'miama, fl', 'tampa, fl', 'tampba bay, fl', 'jacksonville, fl', ' orlando, fl',
                       'miama, florida', 'tampa, florida', 'tampba bay, florida', 'jacksonville, florida',
                       ' orlando, florida']

# Select only Tweets that have a user-defined location in our 'locationsofinterest' list
valid_locs_location = [tweets[i]['user']['location'].lower().replace('\n', ' ').replace('\t', ' ').replace(r"[^\w\s']",' ').strip()
                       in locationsofinterest for i in range(len(tweets))]
valid_tweets_location = list(pd.Series(tweets)[valid_locs_location])

"""### Filter Tweets by Geo-Coordinates Using Reverse GeoCoding"""

# Function to Reverse GeoCode the coordinates to see if they are in Washington or Florida
def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    return result

# Select only Tweets that have Geo-Coordinates
valid_locs_coords = [tweets[i]['coordinates'] != None for i in range(len(tweets))]
valid_tweets_coords = list(pd.Series(tweets)[valid_locs_coords])

# Get a Tuple of all Geo-Coordinates to pass into the reverseGeocode function
tuplecoords = [(valid_tweets_coords[i]['coordinates']['coordinates'][1], valid_tweets_coords[i]['coordinates']['coordinates'][0])
               for i in range(len(valid_tweets_coords))]

# As a check, see where all valid tweet geo-coordinates are located
geometry = [Point(xy) for xy in zip([valid_tweets_coords[i]['coordinates']['coordinates'][0] for i in range(len(valid_tweets_coords))],
                                    [valid_tweets_coords[i]['coordinates']['coordinates'][1] for i in range(len(valid_tweets_coords))])]
geodf = gpd.GeoDataFrame(geometry, columns = ['geometry'])

# Plot the points!
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

geodf.plot(ax=world.plot(figsize=(12,12)), marker = 'o', color = 'red', markersize = 15, alpha = .7)
plt.title('Geographic Coordinates of Twitter Accounts with Tweets Related to COVID-19 & Social Distancing')
plt.ylabel('Latitude')
plt.xlabel('Longitude')
print("It looks like only 1 tweet is in Florida, and 0 are in Washington,\nso we should only capture one tweet")

# Store the place location of all the geo-coordinates
result = []
for i in range(len(valid_tweets_coords)):
    result.append(reverseGeocode(tuplecoords[i]))

# Use the 'admin1' variable from the reverseGeocode to determine the U.S. State of the tweet
state = []
for i in range(len(result)):
    state.append(result[i][0]['admin1'])

# Pick out the indices of the Tweets if the state is Florida or Washington
flindices = [i for i, x in enumerate(state) if x == "Florida"]
waindices = [i for i, x in enumerate(state) if x == 'Washington']

print("List of Tweet indices associated with Florida: {}\nList of Tweet indices associated with Washington: {}".
      format(flindices, waindices))

"""#### We only have 1 valid tweet this time, which matches what we saw from the map."""

# Combine the indices from Florida and Washington into one list
valid_florida = list(pd.Series(valid_tweets_coords)[flindices])
valid_washington = list(pd.Series(valid_tweets_coords)[waindices])
valid_fl_or_wa = valid_florida + valid_washington

"""### Combine all Valid Tweets, Select Only Relevant Variables, Convert to DataFrame, and Store Output as CSV"""

# Further combine all valid geo-coordinates with all of the valid user-defined locations
all_valid_tweets = valid_tweets_location+valid_fl_or_wa

# Each Tweet has 163 variables but we really only need a few; Date created, text of tweet, retweeted text if available,
# the location and coordinates
created_at = [all_valid_tweets[i]['created_at'] for i in range(len(all_valid_tweets))]
full_text = [all_valid_tweets[i]['full_text'] for i in range(len(all_valid_tweets))]
userid = [all_valid_tweets[i]['user']['id'] for i in range(len(all_valid_tweets))]
location = [all_valid_tweets[i]['user']['location'] for i in range(len(all_valid_tweets))]
coordinates = [all_valid_tweets[i]['coordinates'] for i in range(len(all_valid_tweets))]
retweeted_text = []
for i in range(len(all_valid_tweets)):
    try:
        retweeted_text.append(all_valid_tweets[i]['retweeted_status']['full_text'])
    except:
        retweeted_text.append('n/a')

# Store the selected variables in a dataframe
output = pd.DataFrame({'created_at':created_at,'full_text':full_text,'userid':userid,'location':location,
             'coordinates':coordinates,'retweeted_text':retweeted_text})
output.head()

# Save the valid tweets that will later be used for analysis as a csv file
output.to_csv(sample+".csv")

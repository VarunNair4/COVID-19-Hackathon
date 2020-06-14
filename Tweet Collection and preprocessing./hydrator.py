
# Read in necessary libraries and Packages
import os
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import geopandas as gpd
from twarc import Twarc

# Pass in credentials so I can connect to API
t = Twarc(key)


# The JSON file has thousands of JSON objects in it, so we need to first open the file,
# loop through each line, and use the json.loads() function to extract each object
tweets = []
with open('tweets.json') as f:
    for line in f:
        tweets.append(json.loads(line))

len(tweets)

# Printing out the first five tweets in the file
[print(tweets[i]['full_text'],'\n\n') for i in range(5)]

# If a Tweet was retweeted, the text may be shortened. For example, in this tweet below the 'full text'
# is actually cut short, but in the retweeted status we can see the full text.
print(tweets[27]['user']['location'], tweets[27]['full_text']), tweets[27]['retweeted_status']['full_text']

"""### Locations from Tweets"""

# Printing out the first five user locations in the file
[tweets[i]['user']['location'] for i in range(15)]

"""#### Locations are not great, but some users are geo_enabled and have coordinates."""

tweets_coords = []
for i in tweets:
    if i['coordinates'] != None:
        tweets_coords.append(i)

len(tweets_coords)

"""#### 32 Users in this file have a geolocation"""

# Show the coordinates + location for one tweet
tweets_coords[1]['user']['location'], tweets_coords[1]['coordinates']

# Get all lats and lons and store them in a geopandas df for plotting
lats = [tweets_coords[i]['coordinates']['coordinates'][0] for i in range(len(tweets_coords))]
lons = [tweets_coords[i]['coordinates']['coordinates'][1] for i in range(len(tweets_coords))]#
geometry = [Point(xy) for xy in zip(lats, lons)]
geodf = gpd.GeoDataFrame(geometry, columns = ['geometry'])
# Check it works
geodf.head()

# Plot the points!
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

geodf.plot(ax=world.plot(figsize=(15,15)), marker = 'o', color = 'red', markersize = 15)


filenames = []

for file in os.listdir('apriltweets'):
    filename = os.fsdecode(file)
    if filename.endswith( ('.txt') ):
        filenames.append(filename)

ids = []
for file in filenames:
    with open(file,'r') as tweetids:
        ids.append(tweetids.read())

# Write these merged ids
with open('ids.txt', 'w') as outfile:
    for i in ids[0:2]:
        outfile.write(str(i))

ids[0:2]

testids = [ids[0][0:19], ids[0][20:39], ids[0][40:59]]

jsontweets = []
for tweet in t.hydrate(ids[0]):
    jsontweets.append(tweet)

#for tweet in t.hydrate(open('ids.txt')):
#    print(tweet["text"])

jsontweets

testids = ['1245140084313206786', '1245140084350910464', '1245140084417941505']

jsontweets = []
for i in t.hydrate(testids):
    jsontweets.append(i)

jsontweets = json_normalize(jsontweets)

jsontweets[['created_at', 'full_text', 'coordinates', 'user.location', 'retweeted_status.full_text']]

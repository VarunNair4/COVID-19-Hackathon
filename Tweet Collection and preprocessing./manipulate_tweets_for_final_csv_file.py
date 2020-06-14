

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import geopandas as gpd
from pygeocoder import Geocoder
import reverse_geocoder as rg
import glob
import os

"""## Combine all csv Files that were Output in the Previous Steps"""

# Use Glob package to combine all csv files in a directory into one and read them in as a dtaframe
tweets = pd.DataFrame()
for f in glob.glob("random*.csv"):
    df = pd.read_csv(f)
    tweets = all_data.append(df, ignore_index=True)

tweets.head()

tweets.dtypes

# Convert Created At to Date Time
tweets['created_at'] = pd.to_datetime(tweets['created_at'])

print("Number of Days Between First and Last Tweets: {}".format(max(tweets['created_at']) - min(tweets['created_at'])))

plt.figure(figsize = (8,8))
plt.hist(tweets['created_at'], bins = 86)
plt.title('Number of Tweets per Day')

# Create a new column that will have boolean values if the tweet's user-defiend location is in Washington
tweets['Washington'] = [tweets['location'].str.lower()[i] in ['seattle', 'spokane', 'tacoma', 'bellingham', 'tri cities', 'yakima', 'olympia',
                       'wa', 'washington state', 'seattle, wa', 'spokane, wa', 'tacoma, wa', 'bellingham, wa',
                       'tri cities, wa', 'yakima, wa', 'olympia, wa', 'seattle, washington', 'spokane, washington',
                       'tacoma, washington', 'bellingham, washington', 'tri cities, washington', 'yakima, washington',
                       'olympia, washington'] for i in range(len(tweets))]

tweets.head()

# Show the number of tweeets from Wa and Fl
tweets['Washington'].value_counts()

"""### Determine Tweet Location by Geo-Coordinates"""

# Put the non-null coordinates in a dataframe
coordsdf = pd.DataFrame(tweets['coordinates'][pd.notnull(tweets['coordinates'])])

# The Coordinates are brought in as a JSON object
coordsdf

# Get the index position where coordinates are not null
c_ind = coordsdf.index
c_ind

# Turn the JSON objects into a dictionary
coordsdict = pd.DataFrame.to_dict(coordsdf)
# Remove characters to have only the coordinates
coordsdict = [coordsdict['coordinates'][i].split(":")[2].replace("}","").replace("[","").replace("]","").replace("'","") for i in c_ind]

# Split coordinates by the comma to get a latitude and longitude
coords = [coordsdict[i].split(',') for i in range(len(coordsdict))]
lat = [float(coords[i][0]) for i in range(len(coords))]
lon = [float(coords[i][1]) for i in range(len(coords))]
# Store the coordinates in a tuple to pass into the function to reverse GeoCode coorindates
tuplecoords = [(float(coords[i][1]), float(coords[i][0])) for i in range(len(coords))]

# Function to Reverse GeoCode the coordinates to see if they are in Washington or Florida
def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    return result

# Reverse geocode the coordinates to see which state, Washington or Florida, they belong to
result = []
for i in range(len(tuplecoords)):
    result.append(reverseGeocode(tuplecoords[i]))

# Determine which State the Tweet is associated with
state = []
for i in range(len(result)):
    state.append(result[i][0]['admin1'])

# Create a new column in the dataframe that will eventually store the state
tweets['States_Coordinates'] = 'Empty'

# Add the state of the reverse geo-coded coordinates to the new column
tweets.loc[list(c_ind), 'States_Coordinates'] = state

# Replace any 'empty' value in the States_Coordinates column with the value from the Washington column.
tweets.loc[pd.notnull(tweets['coordinates'])][['States_Coordinates', 'Washington']]

# If the States_Coordinates is still empty and the Washington value is true, set the States_Coordinates to Washington,
# otherwise set it to Florida
tweets['States_Coordinates'].loc[(tweets.States_Coordinates == 'Empty') & (tweets.Washington == True)] = 'Washington'
tweets['States_Coordinates'].loc[(tweets.States_Coordinates == 'Empty') & (tweets.Washington == False)] = 'Florida'

# As a check, see where all valid tweet geo-coordinates are located
geometry = [Point(xy) for xy in zip(lat,lon)]
geodf = gpd.GeoDataFrame(geometry, columns = ['geometry'])

# Plot the points!
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

geodf.plot(ax=world.plot(figsize=(12,12)), marker = 'o', color = 'red', markersize = 15, alpha = .7)
plt.title('Geographic Coordinates of Twitter Accounts with Tweets Related to COVID-19 & Social Distancing')
plt.ylabel('Latitude')
plt.xlabel('Longitude')

tweets.loc[(tweets.States_Coordinates != 'Florida') & (tweets.States_Coordinates != 'Washington')]

# We will use their user-defined location to determine which state they belong to
tweets['States_Coordinates'].loc[tweets.States_Coordinates == 'California'] = 'Washington'
tweets['States_Coordinates'].loc[tweets.States_Coordinates == 'Valencia'] = 'Florida'

tweets.States_Coordinates.value_counts()

"""# Store Longer Tweet (Tweet vs Retweet)"""

# Create a new column that will store the longer of the two tweets (tweet vs retweet)
tweets['Full Tweet'] = 'Empty'

print("Retweeted Tweet Length: {}\nTweet Length: {}".format(len(tweets['retweeted_text'][1]), len(tweets['full_text'][1])))

# Find all retweeted tweets and store them in the new column (retweeted are always longer)
tweets['Full Tweet'].loc[pd.notnull(tweets.retweeted_text)] = tweets.retweeted_text

tweets['Full Tweet'].loc[tweets['Full Tweet'] == 'Empty'] = tweets.full_text

tweets.head()

"""# Select the Variables Needed for Analysis: Tweet Timestamp, Text of Tweet, Location of Tweet and Save to csv for Final Analysis"""

# Save the dataframe as the final csv file we will use for analysis
tweets[['created_at', 'Full Tweet', 'States_Coordinates']].to_csv("tweets.csv", encoding = "utf-8", index = False)

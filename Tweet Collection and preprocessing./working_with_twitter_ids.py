

import os
import pandas as pd
import json
import numpy as np
import random
import matplotlib.pyplot as plt


# Read in every single file with twitterids
filenames = []

for file in os.listdir():
    filename = os.fsdecode(file)
    if filename.endswith( ('.txt') ):
        filenames.append(filename)

print("There are {} files, each containing thousands to hundreds of thousands of Twitter IDs".format(len(filenames)))

## ROUND 1 ###
# Open each file, sample 4.5% of tweets, and append them to the ids list
ids = []
for file in filenames:
    with open(file, 'r') as tweetids:
        tweetids = tweetids.read()
        tweetids = tweetids.split('\n')
        ids.append(random.sample(tweetids,int(np.ceil(len(tweetids)*.045))))

# Count number of tweets that were sampled. 4.5% of all tweets were sampled, which
num_tweet_ids = []
for i in ids:
    num_tweet_ids.append(len(i))
print("Randomly Sampling 4.5% of all Tweets amounts to {} Twitter IDs.".format(np.sum(num_tweet_ids)))

plt.title('Histogram of the number of Twitter IDs in each file')
plt.hist(num_tweet_ids)
print("Some Files are Much Larger than Others, which shows 'bursty' activity\nbecause each file is associated with a date and time.")

ids_round1 = ids
used_ids = ids_round1

### ROUND 2 ###
# Open each file, sample 4.5% of tweets, and append them to the ids list
ids = []
for file in filenames:
    with open(file, 'r') as tweetids:
        tweetids = tweetids.read()
        tweetids = tweetids.split('\n')
        tempids = []
        tempids.append(random.sample(tweetids,int(np.ceil(len(tweetids)*.045))))
        for i in tempids:
            if i not in used_ids:
                ids.append(i)

ids_round2 = ids

used_ids = ids_round1 + ids_round2

### ROUND 3 ###
# Open each file, sample 4.5% of tweets, and append them to the ids list
ids = []
for file in filenames:
    with open('C:\\Users\\John\\Desktop\\TwitterIDs\\'+ file, 'r') as tweetids:
        tweetids = tweetids.read()
        tweetids = tweetids.split('\n')
        tempids = []
        tempids.append(random.sample(tweetids,int(np.ceil(len(tweetids)*.045))))
        for i in tempids:
            if i not in used_ids:
                ids.append(i)

ids_round3 = ids

used_ids = ids_round1 + ids_round2 + ids_round3

### ROUND 4 ###
# Open each file, sample 4.5% of tweets, and append them to the ids list
ids = []
for file in filenames:
    with open(file, 'r') as tweetids:
        tweetids = tweetids.read()
        tweetids = tweetids.split('\n')
        tempids = []
        tempids.append(random.sample(tweetids,int(np.ceil(len(tweetids)*.045))))
        for i in tempids:
            if i not in used_ids:
                ids.append(i)

ids_round4 = ids

used_ids = ids_round1 + ids_round2 + ids_round3 + ids_round4

# Write the first 10% of sampled IDs to a new file
with open('randomsample1_round4.txt', 'w') as outfile:
    ids = [item for sublist in ids for item in sublist]
    for i in ids[0:int(len(ids)*.10)]:
        outfile.write(i + '\n')
# Write the 10-20% of sampled IDs to a new file
with open('randomsample2_round4.txt', 'w') as outfile:
    for i in ids[int(len(ids)*.10):int(len(ids)*.20)]:
        outfile.write(i + '\n')

with open('randomsample3_round4.txt', 'w') as outfile:
    for i in ids[int(len(ids)*.20):int(len(ids)*.30)]:
        outfile.write(i + '\n')

with open('randomsample4_round4.txt', 'w') as outfile:
    for i in ids[int(len(ids)*.30):int(len(ids)*.40)]:
        outfile.write(i + '\n')

with open('randomsample5_round4.txt', 'w') as outfile:
    for i in ids[int(len(ids)*.40):int(len(ids)*.50)]:
        outfile.write(i + '\n')

with open('randomsample6_round4.txt', 'w') as outfile:
    for i in ids[int(len(ids)*.50):int(len(ids)*.60)]:
        outfile.write(i + '\n')

with open('randomsample7_round4.txt', 'w') as outfile:
    for i in ids[int(len(ids)*.60):int(len(ids)*.70)]:
        outfile.write(i + '\n')

with open('randomsample8_round4.txt', 'w') as outfile:
    for i in ids[int(len(ids)*.70):int(len(ids)*.80)]:
        outfile.write(i + '\n')

with open('randomsample9_round4.txt', 'w') as outfile:
    for i in ids[int(len(ids)*.80):int(len(ids)*.90)]:
        outfile.write(i + '\n')

with open('randomsample10_round4.txt', 'w') as outfile:
    for i in ids[int(len(ids)*.90)::]:
        outfile.write(i + '\n')


import pandas as pd
import re
import seaborn as sns
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

covid_df= pd.read_csv('tweets.csv')

covid_df.head()

covid_df['Full Tweet']=covid_df['Full Tweet'].replace('\n', ' ', regex=True)

analyzer = SentimentIntensityAnalyzer()

covid_df['rating'] = covid_df['Full Tweet'].apply(analyzer.polarity_scores)
sentiment=pd.concat([covid_df.drop(['rating'], axis=1), covid_df['rating'].apply(pd.Series)], axis=1)

sentiment.loc[sentiment['compound'] >= 0.05, 'Sentiment'] = 1
sentiment.loc[(sentiment['compound'] > -0.05)&(sentiment['compound'] < 0.05), 'Sentiment'] = 0
sentiment.loc[sentiment['compound'] <= -0.05, 'Sentiment'] = -1

sentiment.columns

sentiment.drop(['neg', 'neu', 'pos', 'compound'], axis=1, inplace=True)

df = sentiment
x, y, hue = "Sentiment", "Proportion", "States_Coordinates"
hue_order = ["Washington", "Florida"]
palette = sns.color_palette(['#ff9000','#4E78A0'])

ax=(df[x]
 .groupby(df[hue])
 .value_counts(normalize=True)
 .rename(y)
 .reset_index()
 .pipe((sns.barplot, "data"), x=x, y=y, hue=hue,palette= palette))

ax.set_title('Sentiment Usage')
ax.legend(title="State")
fig1= ax.get_figure()

df['created_at'] = pd.to_datetime(df['created_at']).apply(lambda x: x.date())

df.to_csv("senti.csv")

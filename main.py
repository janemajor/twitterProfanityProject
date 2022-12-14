import tweepy
import pandas as pd
import csv
import re
import matplotlib.pyplot as plt
from flask import (
    Flask,
    jsonify, render_template, session, Response
)
plt.style.use('fivethirtyeight')

#OUR VICTIM
print("What twitter user are we investigating today? ")
target=input()

# get data
keys = pd.read_csv('twitterKeys.csv')

# twitter API keys
consumerKey = keys['Key'][0]
consumerSecret = keys['Key'][1]
accessToken = keys['Key'][2]
accessTokenSecret = keys['Key'][3]

# create authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

# set access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)

# create API object while passing in the auth info
api = tweepy.API(authenticate, wait_on_rate_limit=True)

# extract the tweets! **TEMPORARY TEST RN*
posts = api.user_timeline(screen_name=target, count=100, lang="en", tweet_mode="extended")

# print last five tweets from account **TEMPORARY TEST RN*
#print("Show the 5 recent tweets: \n")
#i=0
#for tweet in posts[0:5]:
 #   i=i+1
 #   print(str(i) + ') ' + tweet.full_text + '\n')

# create dataframe with a column called tweets yeehaw
df = pd.DataFrame([tweet.full_text for tweet in posts], columns = ['Tweets'])

# a function that removes @ and hashtags
def cleanText(text):
    text=text.lower()
    text = re.sub(r'@[A-Za-z0-9]+', '', text) #removes @s
    text = re.sub(r'#', '', text) #removes hashtag
    text = re.sub(r'RT[\s]+', '', text) #rts
    text = re.sub(r'https?:\/\/\S+', '', text) #hyperlinks
    return text

df['Tweets'] = df['Tweets'].apply(cleanText)

#show cleaned text
#print(df)

#bring in the profanity list,
with open("youtubeprofanity2.csv") as f:
    badlist = [row.split()[0] for row in f]
    badlist = list(badlist)
    #badlist = [r'\b' + word + r'\b' for word in badlist]
#print(badlist)


tweetsList =df.values.tolist()
tweetsList= [''.join(x) for x in tweetsList]
#tweetsList=str(tweetsList)
#print(tweetsList)

caughtTweets=[]


#FUNCTION TRIAL 4
def findProfanity(list):
    for word in badlist:
        #print(word)
        for i in list:
            #print(i)
            #print(word)
            for w in i.split():
                #print(w)
                if word.lower() == w.lower():
                    add=str("WORD: " + word + " TWEET: "+ i)
                    caughtTweets.append(add)
    return caughtTweets


print('These tweets go against our community guidelines: \n')
final=findProfanity(tweetsList)
print(final)
print(pd.DataFrame(final))

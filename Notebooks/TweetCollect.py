#Necessary imports
import pandas as pd
import numpy as np
from tqdm import tqdm
import tweepy
from datetime import date
import pickle 
import time

#Get twitter credentials from AppCred.py.
#You must have your own credentials stored in working dir
from AppCred import API_KEY, API_SECRET
from AppCred import ACCESS_TOKEN, ACCESS_TOKEN_SECRET



class BuildTweetDF:
    """
    This class builds a Pandas dataframe using a pickle dump 
    of Tweepy tweet objects as collected by the TweetCollector
    """
    
    def __init__(self, pickle_dump):
        self.all_tweets = self.pickle_open(pickle_dump)
    
    def pickle_open(self, pickle_dump):
        with open(pickle_dump, 'rb') as f:
        # read the data as binary data stream
            all_tweets = pickle.load(f)
        
        return all_tweets
    
    def get_df(self):
        
        final_df_lst = []
        
        for politician, tweets in self.all_tweets.items():
            
            #Empty list for df. More things can be added later
            screen_name = []
            created_at = []
            full_text = []
            favorite_count = []
            retweet_count = []
            tweet_id = []
            in_reply_to_screen_name = []
            hashtags = []
            user_mentions = []
            urls = []
            image = []
            
            for tweet in tweets:
                
                screen_name.append(tweet.user.screen_name)
                created_at.append(tweet.created_at)
                full_text.append(tweet.full_text)
                favorite_count.append(tweet.favorite_count)
                retweet_count.append(tweet.retweet_count)
                tweet_id.append(tweet.id)
                in_reply_to_screen_name.append(tweet.in_reply_to_screen_name)
                
                user_mentions.append([i["screen_name"] for i in tweet.entities["user_mentions"]])
                hashtags.append([i["text"] for i in tweet.entities["hashtags"]])
                
                try:
                    urls.append(tweet.entities["urls"][0]["expanded_url"])
                except:
                    urls.append(np.nan)    
                try:
                    image.append(tweet.entities["media"][3])#["media_url"])
                except:
                    image.append(np.nan)
                            
                
            df = pd.DataFrame({"screen_name":screen_name,
                               "tweet_id":tweet_id,
                               "created_at":created_at,
                               "full_text":full_text,
                               "favorite_count":favorite_count,
                               "retweet_count":retweet_count,
                               "in_reply_to_screen_name":in_reply_to_screen_name,
                               "hashtags":hashtags,
                               "user_mentions":user_mentions,
                               "url":urls,
                               "image_url":image})
            
            #Append politican df to list of all dfs
            final_df_lst.append(df)
            
        #Concat to one final df
        final_df = pd.concat(final_df_lst).reset_index(drop=True)
        
        return final_df
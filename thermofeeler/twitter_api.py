import os
import tweepy
import pandas as pd
from dotenv import load_dotenv, find_dotenv

def twitter_request_test(query,max_results=10):
    env_path = find_dotenv()
    load_dotenv(env_path)

    bearer_token = os.getenv('BEARER_TOKEN')
    client = tweepy.Client(bearer_token=bearer_token)

    # query = '(feliz OR felizmente) lang:pt -aniversário'
    #['word', '"words"', 'word1 OR word2, '@mention', '#hashtag', 'to:account', 'since:year-month-day']
    # queries can be 512 characters long

    tweets = client.search_recent_tweets(query=f'{query} lang:pt',
                                         tweet_fields=['context_annotations', 'created_at'],
                                         max_results=max_results)

    return tweets

def twitter_request(query):
    env_path = find_dotenv()
    load_dotenv(env_path)

    bearer_token = os.getenv('BEARER_TOKEN')
    client = tweepy.Client(bearer_token=bearer_token)
    tweets = tweepy.Paginator(client.search_recent_tweets, query=query,tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000)
    return tweets

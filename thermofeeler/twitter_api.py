import os
import tweepy
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta

def twitter_request_test(query,max_results=10):
    env_path = find_dotenv()
    load_dotenv(env_path)

    bearer_token = os.getenv('BEARER_TOKEN')
    client = tweepy.Client(bearer_token=bearer_token)
    tweets = client.search_recent_tweets(query=f'{query} lang:pt',
                                         tweet_fields=['author_id','created_at','source','entities'],
                                         max_results=max_results)
    return tweets

def twitter_request(query):
    env_path = find_dotenv()
    load_dotenv(env_path)

    bearer_token = os.getenv('BEARER_TOKEN')
    client = tweepy.Client(bearer_token=bearer_token)
    tweets = tweepy.Paginator(client.search_recent_tweets,
                              query=query,
                              tweet_fields=['author_id','created_at','source','entities'],
                              max_results=100).flatten(limit=1000)
    return tweets

def twitter_request_week(query, max_results=20):
    env_path = find_dotenv()
    load_dotenv(env_path)

    bearer_token = os.getenv('BEARER_TOKEN')
    client = tweepy.Client(bearer_token=bearer_token)

    tweets_week = []
    now = datetime.now() + timedelta(hours=3)
    start_time = now - timedelta(days=7)
    end_time = now - timedelta(days=6)

    for loop in range(6):
        tweets = client.search_recent_tweets(query=f'{query} lang:pt',
                                        start_time=start_time,
                                        end_time=end_time,
                                        tweet_fields=['author_id','created_at','source','entities'],
                                        max_results=max_results)
        tweets_week.append(tweets)
        start_time += timedelta(days=1)
        end_time += timedelta(days=1)

    return tweets_week

from thermofeeler import utils
from thermofeeler import twitter_api

def predict_query(query,max_results=10,return_tweets=False):
    '''Receives a query and returns the tweets as well as a dictionary with
    the predictions'''
    print('Getting tweets...')
    tweets=twitter_api.twitter_request_test(query,max_results=max_results)

    print('Organizing tweets...')
    tweets_list=utils.twitter_data(tweets)

    print('Preprocessing tweets...')
    preproc_tweets=[]
    for tweet in tweets_list[0]:
        #tweets_list[0] : list of tweets' text
        preproc_tweets.append(utils.preproc_func(tweet))

    print('Tokenzing tweets...')
    X_test=utils.tokenize_tweets(preproc_tweets)

    print('Predicting sentiments...')
    y_pred=utils.evaluate_tweets(X_test)

    print('Organizing data...')
    eval_dict=utils.get_predicts(y_pred)

    print('Done!')

    if return_tweets==True:
        return tweets_list, eval_dict
    else:
        return eval_dict

def predict_tweet(tweet):
    '''Receives a tweet string and returns a DataFrame with the probabilities
    for each prediction'''

    print('Preprocessing tweet...')
    preproc_tweet=[utils.preproc_func(tweet)]

    print('Tokenzing tweet...')
    X_test=utils.tokenize_tweets(preproc_tweet)

    print('Predicting sentiment...')
    y_pred=utils.evaluate_tweets(X_test)

    print('Organizing predictions...')
    proba=utils.get_proba(y_pred)

    print('Done!')

    return proba.to_dict()

def predict_week(query,max_results=20):
    print('Getting tweets...')
    tweets = twitter_api.twitter_request_week(query,max_results=max_results)

    print('Organizing tweets...')
    tweets_list = utils.twitter_data_week(tweets)

    print('Preprocessing tweets...')
    preproc_tweets=[]
    for tweet in tweets_list[0]: #tweets_list[0] : list of tweets' text
        preproc_tweets.append(utils.preproc_func(tweet))

    print('Tokenzing tweets...')
    X_test = utils.tokenize_tweets(preproc_tweets)

    print('Predicting sentiments...')
    y_pred = utils.evaluate_tweets(X_test)

    print('Organizing data...')
    predict_list = utils.get_predict_order(y_pred)

    return tweets_list, predict_list

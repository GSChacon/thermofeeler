import re

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import models

import numpy as np
import pandas as pd
import pickle

from nltk.tokenize import word_tokenize


# define a preproc function
def preproc_func(tweet):
    '''Does the preprocessing of the tweets'''

    # stopwords: remove articles, prepositions, conjunctions etc
    stopwords=['a','ah','g','h', 'cá','te','tu','tua','tuas','tém','um','uma','você','vocês','vos','à','às','ao','aos',
          'aquela','aquelas','aquele','aqueles','aquilo','as','até','com','como','da','das','de',
          'dela','delas','dele','deles','depois','do','dos','e','ela','elas','ele','eles','em',
          'entre','essa','essas','esse','esses','esta','eu','foi','fomos','for','fora','foram',
          'forem','formos','fosse','fossem','fui','fôramos','fôssemos', 'isso','isto','já','lhe',
          'lhes','me','mesmo','meu','meus','minha','minhas','muito','na','nas','no','nos','nossa',
          'nossas','nosso','nossos','num','numa','nós','oh','o','os','para','pela','pelas','pelo','pelos',
          'por','qual','quando','que','quem','se','seja','sejam','sejamos','sem','serei','seremos',
          'seria','seriam','será','serão','seríamos','seu','seus','somos','sou','sua','suas','são',
          'só','também','ah','q','g','oh','eh','vc','tbm','também','tambem','voceh','você','voce']

    tweet = tweet.lower() # lowercase

    tweet=re.sub('https?://[A-Za-z0-9./]+','',tweet) # remove links que começam com https?://
    tweet=re.sub('https://[A-Za-z0-9./]+','',tweet) # remove links que começam com https://
    tweet=re.sub('http://[A-Za-z0-9./]+','',tweet) # remove links que começam com http://

    tweet = re.sub(r'@[A-Za-z0-9_]+','',tweet) # remove @mentions
    tweet = re.sub(r'#','',tweet) # remove #hashtags

    tweet = re.sub(r'[^\w\s]','',tweet) # remove remove punctuation
    tweet = re.sub(r'[0-9]','',tweet) # remove numbers

    word_tokens=word_tokenize(tweet) # tokenize

    filtered_tweet = [w for w in word_tokens if not w in stopwords] # remove stopwords

    return filtered_tweet

def twitter_data(tweets):
    '''Take the results of the twitter_api results and put them into a list ready to be processed'''

    tweets_search = []
    for tweet in tweets.data :
        tweets_search.append(tweet.text)
    # tweets_search = pd.Series(tweets_search)
    # X_pred = pd.DataFrame(tweets_search, columns=['tweet_text'])

    return tweets_search


def tokenize_tweets(tweets_search):
    '''Tokenize tweets in order to send them to the deep learn model'''

    with open('tokenizer.pickle', 'rb') as handle:
        tk = pickle.load(handle)

    X_test_token = tk.texts_to_sequences(tweets_search)
    X_test = pad_sequences(X_test_token, dtype='float32', padding='post',maxlen=45)

    return X_test

def evaluate_tweets(X_test):
    '''Evaluate the tweets and returns a y_pred'''

    # load model
    model=models.load_model('model')

    # predict y_pred
    y_pred=model.predict(X_test)

    return y_pred

def get_predicts(y_pred):
    '''Returns a dictionary with the final prediction'''

    predict_list = []

    for row in y_pred:
        predict_list.append(np.argmax(row))

    eval_dict={'total': len(predict_list),
          'negative total':predict_list.count(0),
          'neutral total':predict_list.count(1),
          'positive total':predict_list.count(2)}

    return eval_dict

def get_proba(y_pred):
    '''Returns a DataFrame with the probabilities for the y_pred'''

    proba=pd.DataFrame(y_pred,columns=['Negativo','Neutro','Positivo'])

    return proba

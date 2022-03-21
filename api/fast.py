from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from thermofeeler import predict

from google.cloud import storage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Thermofeeler ok!"}

@app.get("/predict_query")
def predict_query(query,max_results=10):

    tweet_list,eval_dict=predict.predict_query(query,
                                    max_results=max_results,
                                    return_tweets=True)

    return tweet_list,eval_dict

@app.get("/predict_tweet")
def predict_tweet(tweet):

    proba=predict.predict_tweet(tweet)

    return proba

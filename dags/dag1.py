import logging
import pendulum
import requests
from airflow.decorators import dag, task, task_group
from airflow.models import Variable
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import pandas as pd
from newsdataapi import NewsDataApiClient
import datetime as dt
from pysentimiento import create_analyzer
from prophet import Prophet
import csv
import duckdb
import yfinance as yf


sentiments = create_analyzer(task="sentiment", lang="en")
emotions = create_analyzer(task='emotion', lang="en")

apikey = "pub_484350d0460b3a6d9a45319e3f2fcfe2f8dc3"



@dag('pleaserun',start_date=dt.datetime.now(), schedule_interval='*/10 * * * *')
def dag1():

    @task
    def get_news():
        try:
            
            api = NewsDataApiClient(apikey=apikey)


            response = api.news_api( q= 's&p500' ,language="en")
            
            articles = pd.DataFrame(response['results'])
            articles = articles[['pubDate', 'title']]
            articles.pubDate = pd.to_datetime(articles.pubDate)
            articles.pubDate = articles.pubDate.apply(lambda x : x.strftime('%Y-%m-%d'))
            articles.pubDate = articles.pubDate.astype(object)
            articles = articles.groupby('pubDate')['title'].sum()
            articles = pd.DataFrame(articles)
            articles = articles.reset_index()
            articles = articles[articles['pubDate'] == str(dt.date.today() - dt.timedelta(days = 1))]
            articles.loc[:,'pubDate'] = str(dt.date.today())
            articles = articles.rename(columns = {'pubDate' : 'ds'})
            return articles


        except Exception as e:
            print(e)
            return None
        
        
    @task
    def get_sentiments(articles):
        
        articles['negative'] = articles['title'].apply(lambda x : sentiments.predict(x).probas['NEG'])
        articles['positive'] = articles['title'].apply(lambda x : sentiments.predict(x).probas['POS'])
        articles['neutral'] = articles['title'].apply(lambda x : sentiments.predict(x).probas['NEU'])
        articles['anger'] = articles['title'].apply(lambda x: emotions.predict(x).probas['anger'])
        articles['disgust'] = articles['title'].apply(lambda x:emotions.predict(x).probas['disgust'])
        articles['fear'] = articles['title'].apply(lambda x:emotions.predict(x).probas['fear'])
        articles['joy'] = articles['title'].apply(lambda x:emotions.predict(x).probas['joy'])
        articles['sadness'] = articles['title'].apply(lambda x:emotions.predict(x).probas['sadness'])
        articles['surprise'] = articles['title'].apply(lambda x:emotions.predict(x).probas['surprise'])
        articles['others'] = articles['title'].apply(lambda x:emotions.predict(x).probas['others'])
        
    
        
        articles = articles[['ds', 'negative', 'positive', 'neutral', 'anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'others']]
        
        articles.to_csv('no_close_fit.csv',index=False)
        
        return articles
            

    @task
    def fit_prediction(articles):
        fit_data = pd.read_csv('/Users/mak/Desktop/Code_With_Me/Sentiment project/Dataset.csv')
        fit_data = fit_data.rename(columns = {'Date': 'ds', 'Close':'y'})
        p = Prophet()
        p.add_regressor('negative')
        p.add_regressor('positive')
        p.add_regressor('neutral')
        p.add_regressor('anger')
        p.add_regressor('disgust')
        p.add_regressor('fear')
        p.add_regressor('joy')
        p.add_regressor('sadness')
        p.add_regressor('surprise')
        p.add_regressor('others')
        p.add_country_holidays(country_name='US')
        
        p.fit(fit_data)
        
        prediction = p.predict(articles)
        
        prediction = prediction[['ds','yhat']]
        
        prediction.ds = prediction.ds.apply(lambda x : x.strftime('%Y-%m-%d'))
        prediction.ds = prediction.ds.astype(object)
        row = list(prediction.iloc[0])
        
        
        
        with open('/Users/mak/Desktop/Code_With_Me/Sentiment project/predictions.csv', 'a', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)
            # Write the new row data
            writer.writerow(row)
            
            
    @task
    def get_sp500():
        
        sp = yf.download("^GSPC", start="2022-01-01", end=dt.date.today())
        
        sp = sp.reset_index()
        
        sp = sp[['Date', 'Close']]
        
        sp.to_csv('sp500.csv',index=False)


    

    articles = get_news()

    articles_sentiments = get_sentiments(articles)

    fit_prediction(articles_sentiments)
    
    get_sp500()
    
    
    

dag1()
        
        
        
            
            
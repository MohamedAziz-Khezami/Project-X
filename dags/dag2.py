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



@dag('night',start_date=dt.datetime(2024,), schedule_interval='0 23 * * 1-5')
def dag2():

    @task
    def new_sp_and_fit():
                
        spnew = yf.download("^GSPC", start="2022-01-01", end=dt.date.today())

        spnew = spnew.reset_index()

        spnew.to_csv('/Users/mak/Desktop/Code_With_Me/Sentiment project/sp500.csv',index=False)

        spn = spnew[['Close']]

        lastclose = spn.iloc[-1]

        lastclose = pd.DataFrame(lastclose).T.reset_index()


        lastclose = lastclose.drop('index', axis=1)


        oldfit = pd.read_csv('/Users/mak/Desktop/Code_With_Me/Sentiment project/no_close_fit.csv')

        new = pd.concat([oldfit, lastclose], axis=1)

        new = new.rename(columns = {'ds' : 'Date'})

        fit_data = pd.read_csv('/Users/mak/Desktop/Code_With_Me/Sentiment project/fit_data.csv')

        fit_data = pd.concat([fit_data, new], axis=0)

        fit_data.to_csv('/Users/mak/Desktop/Code_With_Me/Sentiment project/fit_data.csv', index=False)
                


    new_sp_and_fit()
    
    
dag2()
        
        
    
        

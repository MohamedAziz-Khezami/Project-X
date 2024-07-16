
# 📈Sentimental Stocks

This project combines the unique features of humans and machines that both have a substantial effect on the financal world, which are; emotions, and computational power.
It uses a Facebook powed forecasting algorithm `prophet` and the daily fetched news that get processed to determin their sentimental and emotional weights to predict the daily closing price of the **S&P500 Stocks**.



## Used Libraries

The main libraries used in this project:

- `streamlit`: A python based web framework for quick and easy building and deploymenet of web apps using python language.
- `airflow`: An open-source workflow management platform for data engineering pipelines. 
- `prophet`: A library for producing high quality forecasts for time series data that has multiple seasonality with linear or non-linear growth.
- `pysentimiento`: A Python toolkit for Sentiment Analysis and Social NLP tasks


## API Reference

#### This project used the **News data API**

In this project I used https://newsdata.io to fetch daily news used in predictions.



## Screenshots

The project in use:
![alt text](<Screen Shot 2024-07-16 at 12.21.38 PM.png>)

The project leverages `airflow` schedulers;
- It has a morning dag that runs every morning to fetch yesterday's news, and predict today's s&p500 closing price.
- A night dag that runs every night to retrive the real closing price, and retrain the model using the real data.

![alt text](<Screen Shot 2024-07-16 at 12.28.00 PM.png>)



## Model

You find a detailed jupyter notebook about the used model in the `Stocks.ipynb` file.
- The model was trained on a news data set **from 2008 to 2024**.

![alt text](<Screen Shot 2024-07-16 at 1.44.21 PM.png>)

## Feedback

If you have any feedback, please reach out to us at mohamedazizkhezami@gmail.com



import streamlit as st 
import altair as alt
import datetime as dt
import pandas as pd
import numpy as np
import yfinance as yf


sp500 =yf.download("^GSPC", start="2023-01-01", end="2024-07-12")

sp500 = sp500.reset_index()

sp = sp500[['Date','Close']]

st.set_page_config(
    layout="wide",
    page_title="Sentimental Stocks",
    page_icon="📈",
    )

 
def main():
    
  

    
    
    predictions= pd.read_csv("/Users/mak/Desktop/Code_With_Me/Sentiment project/predictions.csv")
    

    
    
    chart1 = alt.Chart(predictions).mark_circle(color='blue').encode(
    x=alt.X('ds', axis=alt.Axis(title='Date'), type='temporal'),
    y=alt.Y('yhat', axis=alt.Axis(title='Predicted Price')),
    ).interactive()

# Define the second chart
    chart2 = alt.Chart(sp).mark_line(color='red').encode(
    x=alt.X('Date', axis=alt.Axis(title='Date'), type='temporal'),
    y=alt.Y('Close', axis=alt.Axis(title='Closing Price')),
    ).interactive()
    
    # Layer the charts
    combined_chart = alt.layer(chart1, chart2)

# Display the chart in Streamlit
    st.altair_chart(combined_chart, theme=None, use_container_width=True)
    
    

    
    

if __name__ == "__main__":
    main()
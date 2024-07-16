
import streamlit as st 
import altair as alt
import datetime as dt
import pandas as pd
import numpy as np
import yfinance as yf

sp500 =pd.read_csv('/Users/mak/Desktop/Code_With_Me/Sentiment project/assets/sp500.csv')


pred = pd.read_csv('/Users/mak/Desktop/Code_With_Me/Sentiment project/assets/pred.csv')

sp500 = sp500.reset_index()

sp = sp500[['Date','Close']]

st.set_page_config(
    layout="wide",
    page_title="Sentimental Stocks",
    page_icon="📈",
    )

 
def main():
    
    st.title('Sentimental Stocks')
    
    with st.container(border=True):
    
        col1 , col2, col3 = st.columns([3,0.2,1.5])
        
        with col1 :
            predictions= pd.read_csv("/Users/mak/Desktop/Code_With_Me/Sentiment project/assets/predictions.csv")

            chart1 = alt.Chart(predictions).mark_circle(color='blue').encode(
            x=alt.X('ds', axis=alt.Axis(title='Date'), type='temporal'),
            y=alt.Y('yhat', axis=alt.Axis(title='Predicted Price')),
            ).interactive()
            
            chart2 = alt.Chart(sp).mark_line(color='red').encode(
            x=alt.X('Date', axis=alt.Axis(title='Date'), type='temporal'),
            y=alt.Y('Close', axis=alt.Axis(title='Closing Price')),
            ).interactive()
            
            chart3 = alt.Chart(pred).mark_line(color='orange').encode(
            x=alt.X('ds', axis=alt.Axis(title='Date'), type='temporal'),
            y=alt.Y('yhat', axis=alt.Axis(title='Closing Price')),
            ).interactive()
            # Layer the charts
            combined_chart = alt.layer(chart1, chart2,chart3)

        # Display the chart in Streamlit
            st.altair_chart(combined_chart, theme=None, use_container_width=True)
            
            
        with col2:
            st.markdown(
                    '''
                        <div class="divider-vertical-line"></div>
                        <style>
                            .divider-vertical-line {
                                border-left: 2px solid rgba(255, 255, 255, 0.8);
                                height: 320px;
                                margin: auto;
                            }
                        </style>
                    '''
                    , unsafe_allow_html=True
                )

        # Define the second chart

            
        with col3:
            st.title("Stocks News")
            
            news = pd.read_csv('/Users/mak/Desktop/Code_With_Me/Sentiment project/assets/news_feed.csv')
            with st.container(height=230):
                j = 1
                for i in news.title:
                    st.write(j,":",i)
                    j+=1
                    
                
                

        
        
        

    
    


    
    

if __name__ == "__main__":
    main()
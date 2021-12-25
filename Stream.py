import pandas as pd

import streamlit as st
import yfinance as yf
from datetime import date
from plotly import graph_objs as go

import matplotlib as plt

# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split


start = "2010-01-01"
today = date.today().strftime("%Y-%m-%d")

st.title("Forecast Stock Price")

stocks = ("AAPL", "GOOG", "MSFT", "TSLA", "SPY")
selected_stocks = st.selectbox("Выбери акцию для построения прогноза ", stocks)

n_years = st.slider("Период предсказания: ", 1, 4)
period = n_years * 365


# @st.cache
def load_data(ticker):
    df = yf.download(ticker, start, today)
    df.reset_index(inplace=True)
    return df


data_load_state = st.text("Wait ...loading")
df = load_data(selected_stocks)

data_load_state.text("Load ...done! ")

st.header('Raw Date')
st.write(df.tail())


def plot_paint():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='markers', name='g(x)=x',
                             marker=dict(color='LightSkyBlue', size=1.5, line=dict(color='Red', width=1))))
    fig.layout.update(title='Time Series Data', xaxis_rangeslider_visible=True)

    st.plotly_chart(fig)


plot_paint()

# Calculates Moving Average (5) base on stock  price.

st.header('Calculates Moving Average (13) base on stock  price.')
df['ma5'] = df['Close'].rolling(13).mean()
st.line_chart(df['ma5'])

# st.write(df.tail(3))

train_data = df.iloc[5:2700, 7]

# st.write(train_data)
# st.line_chart(train_data)

diff_data = train_data.diff()
diff_data.dropna(inplace=True)

st.header('Calculates the difference of a MA(13) dataframe previous element.')
st.line_chart(diff_data)
# Forecast

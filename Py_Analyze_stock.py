import pandas as pd
import streamlit as st
import yfinance as yf
from datetime import date
from plotly import graph_objs as go

# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
from yfinance import ticker

st.title("Forecast Stock Price Demo Version")

start = st.date_input("Pick a start date")
today = date.today().strftime("%Y-%m-%d")

stocks = ("AAPL", "GOOG", "MSFT", "TSLA", "SPY")
selected_stocks = st.selectbox("Pick a stock ", stocks)

per_ma = ("3", "5", "8", "13", "21", "34")
selected_ma = st.selectbox("Period first MA ", per_ma)

per_ma2 = ("5", "8", "13", "21", "34", "55")
selected_ma2 = st.selectbox("Period second MA ", per_ma2)


# @st.cache
# def load_data(ticker):
#     df = yf.download(ticker, start, today)
#     df.reset_index(inplace=True)
#     return df

def relative(df):
    rel = df.pct_change()
    cumret = (1 + rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret


# data_load_state = st.text("Wait ...loading")
# df = load_data(selected_stocks)
if len(selected_stocks) > 0:
    df = relative(yf.download(selected_stocks, start, today))
    df.reset_index(inplace=True)

# data_load_state.text("Load ...done! ")

st.header('Raw Date')
st.write(df.tail())


def plot_paint():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close']))
    fig.layout.update(title='Time Series Data', xaxis_rangeslider_visible=True)

    st.plotly_chart(fig, use_container_width=True)


plot_paint()

# Calculates Moving Average  base on stock  price.
st.header('Calculates Moving Average  on stock  price.')
df['ma'] = df['Close'].rolling(int(selected_ma)).mean()
df['ma2'] = df['Close'].rolling(int(selected_ma2)).mean()

ma1 = str(selected_ma)
ma2 = str(selected_ma2)

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
stock_concat = pd.concat([df['ma'], df['ma2'], df['Close']], axis=1, keys=['Moving average %s ' % int(selected_ma),
                                                                           'Moving average %s ' % int(selected_ma2),
                                                                           'Close price'
                                                                          ])

st.line_chart(stock_concat)

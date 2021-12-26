import pandas as pd
import streamlit as st
import yfinance as yf
from datetime import date
from plotly import graph_objs as go
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
import matplotlib as plt

# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split


start = "2010-01-01"
today = date.today().strftime("%Y-%m-%d")

st.title("Forecast Stock Price Demo Version")

stocks = ("AAPL", "GOOG", "MSFT", "TSLA", "SPY")
selected_stocks = st.selectbox("Выбери акцию для построения прогноза ", stocks)

per = ("3", "5", "8", "13", "21", "34")
selected_per = st.selectbox("Выбери период МА для построения прогноза ", per)

per_p = ("1", "2", "3", "5", "10", "15", "25", "55")
selected_per_p = st.selectbox("number of lag observations ", per_p)

per_d = ("1", "2", "3", "4", "5", "6")
selected_per_d = st.selectbox("number of times ", per_d)

per_q = ("1", "2", "3", "4", "10", "15", "25", "55")
selected_per_q = st.selectbox("size of the moving average ", per_q)

n_years = st.slider("Период предсказания: ", 5, 30)
period = n_years * 365


# @st.cache
def load_data(ticker):
    df = yf.download(ticker, start, today)
    df.reset_index(inplace=True)
    return df


data_load_state = st.text("Wait ...loading")
df = load_data(selected_stocks)

data_load_state.text("Load ...done! ")

# st.header('Raw Date')
# st.write(df.tail())


def plot_paint():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='markers', name='g(x)=x',
                             marker=dict(color='LightSkyBlue', size=1.5, line=dict(color='Red', width=1))))
    fig.layout.update(title='Time Series Data', xaxis_rangeslider_visible=True)

    st.plotly_chart(fig)


# plot_paint()

# Calculates Moving Average  base on stock  price.

st.header('Calculates Moving Average (%s) base on stock  price.' % (int(selected_per)))
df['ma'] = df['Close'].rolling(int(selected_per)).mean()
# st.line_chart(df['ma'])

diff_data = df.iloc[30:, 7].diff()
diff_data.dropna(inplace=True)

# st.header('Calculates the difference of a MA(%s) with previous element.' % (int(selected_per)))
# st.line_chart(diff_data)

# Prepare Forecast (ACF and PACF)
# st.header('Autocorrelation')
# acf = plot_acf(diff_data, lags=35, use_vlines=True, title='ACF')
# acf.legend([selected_stocks], loc="upper right", fontsize="small", framealpha=1, edgecolor="black", shadow=None)
# st.write(acf)
# pacf = plot_pacf(diff_data, lags=35, use_vlines=True, title='PACF')
# pacf.legend([selected_stocks], loc="upper right", fontsize="small", framealpha=1, edgecolor="black", shadow=None)
# st.write(pacf)

# Forecast
train_data = df.iloc[35:2800, 7]
model = ARIMA(train_data, order=(int(selected_per_p), int(selected_per_d), int(selected_per_q)))
arima = model.fit()
predict_data = arima.predict(2080, 2180, dynamic=True, type='levels')
stock_concat = pd.concat([df['ma'], predict_data], axis=1, keys=['origin', 'predict'])
st.line_chart(stock_concat)

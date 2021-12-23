import streamlit as st
import yfinance as yf

from datetime import date
from plotly import graph_objs as go

start = "2015-01-01"
today = date.today().strftime("%Y-%m-%d")

st.title("Прогнозирование цен акций")

stocks = ("AAPL", "GOOG", "MSFT", "TSLA")
selected_stocks = st.selectbox("Выбери акцию для построения прогноза ", stocks)

n_years = st.slider("Период предсказания: ", 1, 4)
period = n_years*365

@st.cache
def load_data(ticker):
    df = yf.download(ticker,start,today)
    df.reset_index(inplace=True)
    return df
data_load_state = st.text("Подождите ...загрузка")
df = load_data(selected_stocks)

data_load_state.text("Загрузка завершена")

st.header('Котировки')
st.write(df.tail())

st.markdown('## График ')

def plot_paint():
    fig =

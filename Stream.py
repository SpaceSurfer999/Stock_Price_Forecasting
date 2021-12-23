import streamlit as st
import yfinance as yf

from datetime import date
from plotly import graph_objs as go

start = "2015-01-01"
today = date.today().strftime("%Y-%m-%d")

st.title("Forecast Stock Price")

stocks = ("AAPL", "GOOG", "MSFT", "TSLA", "SPY")
selected_stocks = st.selectbox("Выбери акцию для построения прогноза ", stocks)

n_years = st.slider("Период предсказания: ", 1, 4)
period = n_years * 365


@st.cache
def load_data(ticker):
    df = yf.download(ticker, start, today)
    df.reset_index(inplace=True)
    return df


data_load_state = st.text("Wait ...loading")
df = load_data(selected_stocks)

data_load_state.text("Load ...done! ")

st.header('Raw Date')
st.write(df.tail())

st.markdown('## Graph ')


def plot_paint():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close']))
    fig.layout.update(title='Time Series Data', xaxis_rangeslider_visible=True)

    st.plotly_chart(fig)


plot_paint()

# st.line_chart(df['Close'])

import streamlit as st
import yfinance as yf
import pandas as pd
#import pandas_ta as ta
import plotly.graph_objects as go

st.set_page_config(page_title="Jitendra AI Trading", layout="wide")
st.title("📈 Jitendra Singh's AI Trading Agent")

symbol = st.sidebar.text_input("Stock Symbol (e.g. RELIANCE.NS)", value="RELIANCE.NS")

if symbol:
    data = yf.download(symbol, period="5d", interval="15m")
    if not data.empty:
        last_price = float(data['Close'].iloc[-1])
        st.metric(label=f"{symbol} Current Price", value=f"₹{last_price:.2f}")

        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'], high=data['High'],
                        low=data['Low'], close=data['Close'])])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Data not found!")

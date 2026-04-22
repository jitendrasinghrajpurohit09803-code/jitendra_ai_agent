import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Jitendra AI Trading", layout="wide")
st.title("📈 Jitendra Singh's AI Trading Agent")

symbol = st.sidebar.text_input("Enter Symbol (e.g. RELIANCE.NS)", value="RELIANCE.NS")

if symbol:
    try:
        # डेटा को साफ़ तरीके से डाउनलोड करना
        data = yf.download(symbol, period="5d", interval="15m", group_by='column')
        
        if not data.empty:
            # डेटा को सरल (Flatten) बनाना ताकि एरर न आए
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            # आखिरी क्लोजिंग प्राइस निकालना
            last_price = float(data['Close'].iloc[-1])
            st.metric(label=f"Current Price: {symbol}", value=f"₹{last_price:.2f}")
            
            # कैंडलस्टिक चार्ट
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close']
            )])
            
            fig.update_layout(xaxis_rangeslider_visible=False, title=f"Live Performance: {symbol}")
            st.plotly_chart(fig, use_container_width=True)
            st.success("बाज़ार का डेटा सफलतापूर्वक लोड हो गया है!")
        else:
            st.warning("डेटा नहीं मिला। कृपया सिंबल चेक करें।")
    except Exception as e:
        st.error(f"Error: {e}")

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from gtts import gTTS
import base64
from io import BytesIO

st.set_page_config(page_title="Jitendra AI Voice Agent", layout="wide")
st.title("🎙️ Jitendra's AI Voice Agent")

# आवाज़ निकालने वाला फंक्शन
def say_something(text):
    tts = gTTS(text=text, lang='hi') # हिंदी भाषा
    fp = BytesIO()
    tts.write_to_fp(fp)
    return fp

symbol = st.sidebar.text_input("शेयर का नाम लिखें", value="RELIANCE.NS")

if symbol:
    data = yf.download(symbol, period="1d", interval="15m")
    if not data.empty:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        last_price = float(data['Close'].iloc[-1])
        st.metric(label=f"Current Price: {symbol}", value=f"₹{last_price:.2f}")
        
        # आवाज़ का बटन
        msg = f"जितेंद्र, {symbol} की ताज़ा कीमत {last_price:.2f} रुपए है।"
        if st.button("आवाज़ में सुनें 🔊"):
            sound_fp = say_something(msg)
            st.audio(sound_fp, format='audio/mp3')
            
        # चार्ट
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
        st.plotly_chart(fig, use_container_width=True)

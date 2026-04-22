import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="Jitendra AI Jarvis", layout="wide")
st.title("🎙️ Jitendra Singh's AI Jarvis")

# आवाज़ पैदा करने वाला फंक्शन
def speak(text):
    tts = gTTS(text=text, lang='hi')
    fp = BytesIO()
    tts.write_to_fp(fp)
    return fp

# मॉर्निंग ब्रीफिंग फंक्शन (एरर फ्री)
def get_morning_briefing():
    nifty = yf.download("^NSEI", period="1d", interval="1m")
    if not nifty.empty:
        # डेटा को साफ़ तरीके से निकालना
        if isinstance(nifty.columns, pd.MultiIndex):
            nifty.columns = nifty.columns.get_level_values(0)
        
        current_val = float(nifty['Close'].iloc[-1])
        report = f"सुप्रभात बॉस! मार्केट खुल चुका है। निफ्टी अभी {current_val:.2f} पर ट्रेड कर रहा है। आज सावधानी से काम करें।"
        return report, current_val
    return "बॉस, अभी डेटा नहीं मिल पा रहा है।", 0

# साइडबार में बटन
if st.sidebar.button("Morning Briefing 🎙️"):
    text_report, val = get_morning_briefing()
    st.subheader("आज की रिपोर्ट:")
    st.write(text_report)
    
    # आवाज़ सुनाना
    audio_fp = speak(text_report)
    st.audio(audio_fp, format='audio/mp3')

# सामान्य चार्ट कोड
symbol = st.sidebar.text_input("Enter Symbol", value="RELIANCE.NS")
if symbol:
    data = yf.download(symbol, period="5d", interval="15m")
    if not data.empty:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        st.metric(label=f"Price: {symbol}", value=f"₹{float(data['Close'].iloc[-1]):.2f}")
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
        st.plotly_chart(fig, use_container_width=True)

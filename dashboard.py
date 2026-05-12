import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import time

st.set_page_config(page_title="Jitendra AI Agent", layout="wide")

# यहाँ अपनी कॉपी की हुई चाबी को " " के बीच पेस्ट करें
DID_API_KEY = "Q1BAYR9KDq9ANJBL"

def create_ai_video(text):
    url = "https://api.d-id.com/talks"
    headers = {"Authorization": f"Basic {DID_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "script": {
            "type": "text",
            "provider": {"type": "microsoft", "voice_id": "hi-IN-SwaraNeural"},
            "input": text
        },
        "source_url": "https://create-images-results.d-id.com/api_docs/woman.jpg"
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.json().get("id")

def get_video_url(talk_id):
    url = f"https://api.d-id.com/talks/{talk_id}"
    headers = {"Authorization": f"Basic {DID_API_KEY}"}
    for _ in range(10):
        res = requests.get(url, headers=headers).json()
        if res.get("result_url"): return res.get("result_url")
        time.sleep(3)
    return None

st.title("🎙️ Jitendra Singh's Digital AI Agent")

if st.sidebar.button("Morning Briefing 🎙️"):
    with st.spinner("बॉस, रिपोर्ट तैयार हो रही है..."):
        data = yf.download("^NSEI", period="1d")
        # डेटा निकालने का सबसे सुरक्षित तरीका
        last_price = data['Close'].iloc[-1]
        if hasattr(last_price, 'iloc'): last_price = last_price.iloc[0]
        
        msg = f"नमस्ते जीतेन्द्र बॉस! मार्केट खुल चुका है। निफ्टी अभी {float(last_price):.2f} पर है। आपका दिन शुभ हो।"
        
        v_id = create_ai_video(msg)
        v_url = get_video_url(v_id)
        if v_url: st.video(v_url)
        else: st.error("वीडियो बनाने में देरी हो रही है।")

symbol = st.sidebar.text_input("Stock Name", value="RELIANCE.NS")
if symbol:
    stock_data = yf.download(symbol, period="5d")
    st.line_chart(stock_data['Close'])

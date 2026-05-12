import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import time

# --- सेटिंग्स ---
st.set_page_config(page_title="Jitendra AI Agent", layout="wide")
DID_API_KEY = "Q1BAYR9KDq9ANJBL" # यहाँ अपनी की पेस्ट करें

# --- अवतार फंक्शन ---
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

# --- इंटरफेस ---
st.title("🎙️ Jitendra Singh's Digital AI Agent")

if st.sidebar.button("Morning Briefing 🎙️"):
    with st.spinner("बॉस, रिपोर्ट तैयार हो रही है..."):
        data = yf.download("^NSEI", period="1d")
        price = float(data['Close'].iloc[-1])
        msg = f"नमस्ते जीतेन्द्र बॉस! मार्केट खुल चुका है। निफ्टी अभी {price:.2f} पर है। आपका दिन शुभ हो।"
        
        v_id = create_ai_video(msg)
        v_url = get_video_url(v_id)
        if v_url: st.video(v_url)

symbol = st.sidebar.text_input("Stock Name", value="RELIANCE.NS")
if symbol:
    stock_data = yf.download(symbol, period="5d")
    st.line_chart(stock_data['Close'])

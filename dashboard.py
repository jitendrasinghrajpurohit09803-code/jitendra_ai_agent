import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import time

st.set_page_config(page_title="Jitendra Singh AI", layout="wide")

# अपनी API Key यहाँ डालें (Basic के बाद अपनी चाबी पेस्ट करें)
# उदाहरण: "Basic Y29tYXBpZGV2ZWxvcGVyQGdtYWlsLmNvbTpkZklkZ..."
DID_API_KEY = "यहाँ_अपनी_पूरी_Key_पेस्ट_करें"

def create_ai_video(text):
    url = "https://api.d-id.com/talks"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }
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
    
    # वीडियो बनने में थोड़ा समय लगता है (बाड़मेर के धैर्य की परीक्षा!)
    for _ in range(15):
        res = requests.get(url, headers=headers).json()
        if res.get("result_url"):
            return res.get("result_url")
        time.sleep(3)
    return None

st.title("🎙️ Jitendra Singh's Digital AI Agent")

# मॉर्निंग ब्रीफिंग बटन
if st.sidebar.button("बात करें (AI Avatar) 🎙️"):
    with st.spinner("आपका डिजिटल एजेंट तैयार हो रहा है..."):
        # निफ्टी का डेटा लेना
        nifty = yf.download("^NSEI", period="1d", interval="1m")
        if not nifty.empty:
            price = float(nifty['Close'].iloc[-1])
            msg = f"नमस्ते जीतेन्द्र सर! मार्केट खुल गया है। निफ्टी अभी {price:.2f} पर चल रहा है। आज का दिन आपके लिए मंगलमय हो।"
            
            talk_id = create_ai_video(msg)
            video_url = get_video_url(talk_id)
            
            if video_url:
                st.video(video_url)
                st.success("लीजिए बॉस, आपकी रिपोर्ट!")
            else:
                st.error("वीडियो प्रोसेस होने में समय लग रहा है, कृपया एक बार फिर बटन दबाएँ।")

# चार्ट वाला हिस्सा
symbol = st.sidebar.text_input("शेयर चुनें", value="RELIANCE.NS")
if symbol:
    data = yf.download(symbol, period="5d")
    if not data.empty:
        st.subheader(f"{symbol} का 5 दिनों का चार्ट")
        st.line_chart(data['Close'])

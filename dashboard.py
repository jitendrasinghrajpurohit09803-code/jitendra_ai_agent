import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
import requests
import time
import pandas as pd

# --- 1. अपनी API Keys यहाँ भरें ---
GEMINI_KEY = "AIzaSyCJ9sndNTHRir4nfcUh1Jgp8JV89jxMZQI"      
DID_API_KEY = "Basic rn3MnAxUQifXv5l_mOtr" # 'Basic ' ज़रूर लगायें

# --- कॉन्फ़िगरेशन ---
genai.configure(api_key=GEMINI_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Jitendra AI Trader", layout="wide")
st.title("🛡️ Jitendra Singh's AI Chart Analyzer")

# --- फंक्शन: D-ID वीडियो बनाना ---
def create_ai_video(text):
    url = "https://api.d-id.com/talks"
    headers = {
        "Authorization": DID_API_KEY, 
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
    try:
        res = requests.post(url, json=payload, headers=headers)
        return res.json().get("id")
    except:
        return None

def get_video_url(talk_id):
    if not talk_id: return None
    url = f"https://api.d-id.com/talks/{talk_id}"
    headers = {"Authorization": DID_API_KEY}
    for _ in range(10):
        res = requests.get(url, headers=headers).json()
        if res.get("result_url"): return res.get("result_url")
        time.sleep(3)
    return None

# --- मुख्य इंटरफेस ---
st.header("📸 Visual Market Analysis")
st.write("अपने ट्रेडिंग चार्ट का स्क्रीनशॉट अपलोड करें और AI से सलाह लें।")

uploaded_file = st.file_uploader("यहाँ फोटो डालें (JPG, PNG)", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        img = Image.open(uploaded_file)
        st.image(img, caption="आपका चार्ट", use_container_width=True)
    
    with col2:
        if st.button("चार्ट एनालाइज करें 🔍"):
            with st.spinner("AI चार्ट का बारीकी से अध्ययन कर रहा है..."):
                prompt = "आप एक प्रोफेशनल ट्रेडर हैं। इस चार्ट का हिंदी में टेक्निकल एनालिसिस करें। सपोर्ट, रेजिस्टेंस, कैंडलस्टिक पैटर्न और अगला मूव बताएं।"
                response = vision_model.generate_content([prompt, img])
                st.session_state.analysis_text = response.text
                st.success("एनालिसिस तैयार!")
                st.write(st.session_state.analysis_text)
        
        if 'analysis_text' in st.session_state:
            if st.button("अवतार से रिपोर्ट सुनें 🎙️"):
                with st.spinner("वीडियो बन रहा है..."):
                    # छोटा मैसेज भेज रहे हैं ताकि क्रेडिट बचे
                    short_msg = st.session_state.analysis_text[:250]
                    v_id = create_ai_video(short_msg)
                    v_url = get_video_url(v_id)
                    if v_url: st.video(v_url)
                    else: st.error("वीडियो नहीं बन पाया। कृपया D-ID क्रेडिट चेक करें।")

# --- मार्केट डेटा (Sidebar) ---
st.sidebar.header("Live Tracker")
symbol = st.sidebar.text_input("Stock Symbol (e.g. RELIANCE.NS)", value="^NSEI")
if symbol:
    data = yf.download(symbol, period="5d")
    st.sidebar.line_chart(data['Close'])

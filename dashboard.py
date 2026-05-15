import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
import requests
import time
from streamlit_vapi import vapi

# --- 1. अपनी सभी API Keys यहाँ भरें ---
GEMINI_KEY = "AIzaSyCJ9sndNTHRir4nfcUh1Jgp8JV89jxMZQI"      # Google AI Studio से
DID_API_KEY = "Basic rn3MnAxUQifXv5l_mOtrJ"      # D-ID से ('Basic ' के साथ)
VAPI_PUBLIC_KEY = "f..." # Vapi.ai से
VAPI_ASSISTANT_ID = "f.."  # Vapi के 'Relay' की ID

# --- कॉन्फ़िगरेशन ---
genai.configure(api_key=GEMINI_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Jitendra Super-AI", layout="wide")
st.title("🚀 Jitendra Singh's Super-AI Trading Agent")

# --- फंक्शन: D-ID वीडियो बनाना ---
def create_ai_video(text):
    url = "https://api.d-id.com/talks"
    headers = {"Authorization": DID_API_KEY, "Content-Type": "application/json"}
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
    headers = {"Authorization": DID_API_KEY}
    for _ in range(10):
        res = requests.get(url, headers=headers).json()
        if res.get("result_url"): return res.get("result_url")
        time.sleep(3)
    return None

# --- लेआउट ---
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📸 Visual Chart Analysis")
    uploaded_file = st.file_uploader("चार्ट का स्क्रीनशॉट यहाँ अपलोड करें", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="आपका चार्ट", use_container_width=True)
        
        if st.button("AI से चार्ट एनालाइज कराएं"):
            with st.spinner("AI चार्ट देख रहा है..."):
                prompt = "आप एक प्रो ट्रेडर हैं। इस चार्ट का हिंदी में टेक्निकल एनालिसिस करें। सपोर्ट, रेजिस्टेंस और एंट्री पॉइंट बताएं।"
                response = vision_model.generate_content([prompt, img])
                analysis_text = response.text
                st.success("एनालिसिस तैयार है!")
                st.write(analysis_text)
                
                # एनालिसिस को वीडियो में बदलना
                if st.button("इसे अवतार से सुनिए 🎙️"):
                    v_id = create_ai_video(analysis_text[:200]) # छोटा मैसेज ताकि क्रेडिट कम लगें
                    v_url = get_video_url(v_id)
                    if v_url: st.video(v_url)

with col2:
    st.header("📞 Live Voice Agent")
    st.write("बाजार पर चर्चा करने के लिए 'Talk' बटन दबाएं:")
    # Vapi बटन
    vapi(public_key=VAPI_PUBLIC_KEY, assistant_id=VAPI_ASSISTANT_ID)

# --- मार्केट डेटा (Sidebar) ---
st.sidebar.header("Live Tracker")
symbol = st.sidebar.text_input("Stock Symbol", value="^NSEI")
if symbol:
    data = yf.download(symbol, period="5d")
    st.sidebar.line_chart(data['Close'])

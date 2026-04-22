import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import time

st.set_page_config(page_title="Jitendra AI Avatar", layout="wide")

# यहाँ अपनी API Key डालें
DID_API_KEY = "

# API Keys

Get your API key from the Studio in four steps

Get your API key from the [Studio](https://studio.d-id.com). Use it to authenticate all API requests.

<CoolSteps name="generate-api-key">
  <CoolStep number={1} title="Log into the Studio">
    Sign in at [studio.d-id.com](https://studio.d-id.com).
  </CoolStep>

  <CoolStep number={2} title="Go to Account settings">
    Open [Account settings](https://studio.d-id.com/account-settings).
  </CoolStep>

  <CoolStep number={3} title="Generate API key and store securely">
    Click Generate API key. The key (format: `API_USER:API_PASSWORD`) is shown only once - copy it and save it in a secure place.
  </CoolStep>

  <CoolStep number={4} title="Use your key in requests">
    Send your key in the `Authorization` header as `Basic API_USER:API_PASSWORD` with every API request.

    ```yaml Request
    curl -X GET "https://api.d-id.com/agents" \
      -H "Authorization: Basic <YOUR KEY>"
    ```
  </CoolStep>
</CoolSteps>"

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
    for _ in range(15):
        res = requests.get(url, headers=headers).json()
        if res.get("result_url"):
            return res.get("result_url")
        time.sleep(3)
    return None

st.title("🎙️ Jitendra Singh's Digital AI Agent")

if st.sidebar.button("Morning Briefing (Avatar) 🎙️"):
    with st.spinner("बॉस, आपका AI अवतार तैयार हो रहा है..."):
        # मार्केट डेटा (सुरक्षित तरीका)
        nifty = yf.download("^NSEI", period="1d")
        if not nifty.empty:
            # डेटा को सीधा नंबर में बदलना
            last_val = nifty['Close'].values[-1]
            if isinstance(last_val, (list, pd.Series, pd.Index)):
                last_val = last_val[0]
            
            msg = f"नमस्ते जीतेन्द्र बॉस! मार्केट खुल चुका है। निफ्टी अभी {float(last_val):.2f} पर है। आज का दिन आपके लिए मंगलमय हो।"
            
            talk_id = create_ai_video(msg)
            video_url = get_video_url(talk_id)
            
            if video_url:
                st.video(video_url)
                st.success("रिपोर्ट तैयार है, बॉस!")
            else:
                st.error("वीडियो बनाने में समय लग रहा है, कृपया दोबारा दबाएँ।")

# चार्ट वाला हिस्सा
symbol = st.sidebar.text_input("Stock Symbol", value="RELIANCE.NS")
if symbol:
    data = yf.download(symbol, period="5d")
    if not data.empty:
        st.line_chart(data['Close'])

import streamlit as st
import requests
from datetime import datetime
import time

BOT_TOKEN = "8781392368:AAH1A5P_2wjt5w9jOEWrSeK-eaGIqB2S7Tg"
CHAT_ID = "1482959961"

st.set_page_config(page_title="FINEST AI v106", layout="wide")
st.title("👑 FINEST AI v106 - LIVE")

def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except:
        pass

st.success(f"LIVE ✅ {datetime.now().strftime('%H:%M:%S')}")

if st.checkbox("FULL AUTO ON (15 Min)", value=True):
    send_tg(f"🚀 LIVE GOLD BUY 4392 T1 4398 T2 4404 T3 4410 SL 4382 | {datetime.now().strftime('%H:%M')}")
    st.write("✅ Sent! Next in 15 min")
    time.sleep(900)
    st.rerun()

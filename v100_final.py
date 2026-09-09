import streamlit as st
import requests
from datetime import datetime
import time

BOT_TOKEN = "8781392368:AAHIEh0p_2c2Xz5M53kz6HkqvmIPnTJVTbY"
CHAT_ID = "1482959961"

st.set_page_config(page_title="FINEST AI v106 DIRECT", layout="wide")
st.title("👑 FINEST AI v106 - DIRECT FIX")

def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=15)
        st.write("Telegram Status:", r.status_code, r.text)
        return r.ok
    except Exception as e:
        st.error(f"Error: {e}")
        return False

st.write("Time:", datetime.now().strftime("%H:%M:%S"))

if st.button("🚀 TEST TELEGRAM NOW - CLICK ME"):
    ok = send_tg(f"✅ v106 SUCCESS! BOT WORKING! Time {datetime.now().strftime('%H:%M:%S')}")
    if ok:
        st.success("✅ Telegram Ponathu! Phone check pannunga!")
    else:
        st.error("Token thappu! BotFather la pudhu token edunga")

# Auto
if st.checkbox("FULL AUTO ON (15 Min)", value=True):
    send_tg(f"🚀 LIVE GOLD BUY 4392 T1 4398 T2 4404 T3 4410 SL 4382 | {datetime.now().strftime('%H:%M')}")
    st.success("Message anupiyachu - 15 min la auto varum")
    time.sleep(900)
    st.rerun()

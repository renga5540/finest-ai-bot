import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(page_title="FINEST AI v105 FIXED", layout="wide")
st.title("👑 FINEST AI v105 - NO MORE ERROR")

# SAFE SECRET CHECK - KeyError varaathu
BOT_TOKEN = st.secrets.get("8781392368:AAHIEh0p_2c2Xz5M53kz6HkqvmIPnTJVTbY", "")
CHAT_ID = st.secrets.get("1482959961", "")

if not BOT_TOKEN or not CHAT_ID:
    st.error("❌ SECRETS ILLA! Keela step follow pannunga")
    st.code('BOT_TOKEN = "123456:AA..."\nCHAT_ID = "1482959961"', language="toml")
    st.info("Manage app -> Settings -> Secrets la itha paste pannunga")
    st.stop()

def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{8781392368:AAHIEh0p_2c2Xz5M53kz6HkqvmIPnTJVTbY}/sendMessage"
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        return f"OK - {r.status_code}"
    except Exception as e:
        return str(e)

st.success(f"✅ Secrets OK! Chat ID: {CHAT_ID}")
st.write("Time:", datetime.now().strftime("%d/%m %H:%M:%S"))

if st.button("✅ TEST TELEGRAM NOW"):
    res = send_tg(f"✅ v105 FIXED SUCCESS! Time: {datetime.now().strftime('%H:%M:%S')}")
    st.write(res)
    st.success("Telegram pochu - Check pannunga!")

# AUTO
auto = st.toggle("FULL AUTO ON (15 Min)", value=True)
if auto:
    send_tg(f"🚀 LIVE - GOLD Entry 4392 T1 4398 T2 4404 T3 4410 SL 4382 - {datetime.now().strftime('%H:%M:%S')}")
    st.success("Message Anupiyachu!")
    time.sleep(900)
    st.rerun()

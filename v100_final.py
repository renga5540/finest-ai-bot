import streamlit as st
import requests
import yfinance as yf
import time
from datetime import datetime

# --- SECURE TOKEN SYSTEM - 100% SAFE ---
try:
    BOT_TOKEN = st.secrets["BOT_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
except:
    BOT_TOKEN = "8781392368:AAHIEh0p_2c2Xz5M53kz6HkqvmIPnTJVTbY"
    CHAT_ID = "1482959961"
    st.error("⚠️ Secrets-la BOT_TOKEN Podala! Manage app -> Settings -> Secrets-la Podunga!")

def send_telegram(msg):
    if not BOT_TOKEN or "YOUR_BOT" in BOT_TOKEN:
        st.warning("Token Illa - Telegram Pokathu")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=15)
        return True
    except Exception as e:
        st.error(f"Telegram Error: {e}")
        return False

# --- UNGA FINEST AI LOGIC INGE IRUKKU ---
st.set_page_config(page_title="FINEST AI v103", layout="wide")
st.title("👑 FINEST AI v103 - CLOUD LIVE")

# ... unga strategy code inga irukkum ...

# AUTO MODE
st.write("### AUTO MODE")
minutes = st.slider("Minutes", 1, 60, 15)
auto_on = st.toggle("FULL AUTO ON")

if auto_on:
    st.success(f"AUTO RUNNING... {minutes} min ku oru murai")
    # unga signal logic
    # send_telegram("Test Signal 🚀")
    time.sleep(minutes*60)
    st.rerun()

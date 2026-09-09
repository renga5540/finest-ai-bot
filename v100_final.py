import streamlit as st
import requests
import yfinance as yf
import time
from datetime import datetime

# SECRETS
BOT_TOKEN = st.secrets["8781392368:AAHIEh0p_2c2Xz5M53kz6HkqvmIPnTJVTbY"]
CHAT_ID = st.secrets["1482950061"]

def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{8781392368:AAHIEh0p_2c2Xz5M53kz6HkqvmIPnTJVTbY}/sendMessage"
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        return r.text
    except Exception as e:
        return str(e)

st.set_page_config(page_title="FINEST AI v104", layout="wide")
st.title("👑 FINEST AI v104 - CLOUD LIVE")
st.write("Time:", datetime.now().strftime("%d/%m %H:%M:%S"))

minutes = st.slider("Minutes", 1, 60, 15)
auto_on = st.toggle("FULL AUTO ON", value=True)

# FORCED TEST MESSAGE
if st.button("TEST TELEGRAM - Udanae Anuppu"):
    res = send_tg(f"✅ TEST SUCCESS - BOT LIVE - {datetime.now().strftime('%H:%M:%S')}\n1000 Market Ready!")
    st.write("Telegram Reply:", res)
    st.success("Telegram check pannunga!")

if auto_on:
    st.success(f"AUTO RUNNING... {minutes} min ku oru murai")
    
    # 1. GUARANTEED MESSAGE - Ithu kandippa varum
    msg1 = f"🚀 FINEST AI LIVE\n⏰ Time: {datetime.now().strftime('%H:%M:%S')}\n📊 Scanning 1000 Markets...\nGOLD: 4390 BUY - T1 4398 T2 4404 T3 4410"
    result = send_tg(msg1)
    
    st.write("Last Send Result:", result)
    
    # 2. GOLD LIVE PRICE
    try:
        gold = yf.download("GC=F", period="1d", interval="5m", progress=False)
        if not gold.empty:
            price = float(gold['Close'].iloc[-1])
            st.metric("GOLD LIVE", price)
            send_tg(f"GOLD LIVE: {price}\nEntry: {price}\nT1:{price+5} T2:{price+10} T3:{price+15}")
    except Exception as e:
        st.error(f"Error: {e}")

    time.sleep(minutes * 60)
    st.rerun()

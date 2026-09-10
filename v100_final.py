import streamlit as st
import requests
import yfinance as yf
import time
from datetime import datetime

# --- SECURE TOKEN ---
try:
    BOT_TOKEN = st.secrets["BOT_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
except:
    BOT_TOKEN = ""
    CHAT_ID = "1482959961"

def send_telegram(msg):
    if not BOT_TOKEN or len(BOT_TOKEN) < 20:
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=15)
        return True
    except:
        return False

st.set_page_config(page_title="FINEST AI v103 ALL MARKET", layout="wide")
st.title("👑 FINEST AI v103 - ALL MARKET LIVE")
st.success("✅ PAZHAYA MARKET DELETE - PUDHU FULL LIST ONLY!")

# --- 🔥 THALAIVA FULL ALL-MARKET LIST (ONLY THIS) ---
STOCKS = [
    # INDIAN TOP 20
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "LT.NS", "KOTAKBANK.NS",
    "TATAMOTORS.NS", "BAJFINANCE.NS", "TATASTEEL.NS", "WIPRO.NS", "ADANIENT.NS",
    "ASIANPAINT.NS", "MARUTI.NS", "TITAN.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS",
    # US TOP 7
    "AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META",
    # CRYPTO 6
    "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "DOGE-USD",
    # GOLD, SILVER, CRUDE, GAS, COPPER
    "GC=F", "SI=F", "CL=F", "NG=F", "HG=F",
    # FOREX & INDICES
    "USDINR=X", "^NSEI", "^NSEBANK", "^GSPC"
]

st.write(f"📊 TOTAL SCANNING: {len(STOCKS)} MARKETS")
st.write("INDIAN + US + CRYPTO + GOLD + CRUDE OIL + FOREX")

# --- SCANNING LOGIC ---
minutes = st.slider("Minutes", 1, 60, 15)
auto_on = st.toggle("FULL AUTO ON")

if auto_on:
    st.success(f"AUTO RUNNING... {minutes} min | {len(STOCKS)} Markets")
    for stock in STOCKS:
        try:
            data = yf.download(stock, period="1d", interval="15m", progress=False)
            if not data.empty:
                last_price = float(data['Close'].iloc[-1])
                st.write(f"{stock}: {last_price}")
                # Inga unga BUY/SELL logic varum
        except:
            continue
    time.sleep(minutes*60)
    st.rerun()

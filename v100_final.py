import streamlit as st, yfinance as yf, requests
import pandas as pd
from datetime import datetime

BOT_TOKEN = st.secrets.get("BOT_TOKEN", "8781392368:AAHIEh0p_2c2Xz5M53kzGHkqvmIPnTJVTbY")
CHAT_ID = st.secrets.get("CHAT_ID", "1482959961")

st.set_page_config(page_title="CORRECT SIGNALS ONLY v700", layout="wide")
st.title("✅ CORRECT INFO ONLY - Market Kudutha Mattum Entry")
st.success("No Random! Market tharum pothu mattum signal!")

def send_tg(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try: requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except: pass

def get_correct_signal(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="15m", progress=False)
        if len(df) < 50: return None
        
        close = df['Close']
        ema9 = close.ewm(span=9).mean()
        ema21 = close.ewm(span=21).mean()
        
        # RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        last_price = float(close.iloc[-1])
        last_ema9 = float(ema9.iloc[-1])
        last_ema21 = float(ema21.iloc[-1])
        last_rsi = float(rsi.iloc[-1])
        
        # CORRECT LOGIC - Market kudutha mattum
        if last_ema9 > last_ema21 and last_rsi > 55 and last_rsi < 75:
            # BUY - Strong
            sl = last_price * 0.986
            t1 = last_price * 1.012
            t2 = last_price * 1.025
            t3 = last_price * 1.04
            return f"BUY", last_price, sl, t1, t2, t3, last_rsi
        elif last_ema9 < last_ema21 and last_rsi < 45 and last_rsi > 25:
            sl = last_price * 1.014
            t1 = last_price * 0.988
            t2 = last_price * 0.975
            t3 = last_price * 0.96
            return f"SELL", last_price, sl, t1, t2, t3, last_rsi
        else:
            return None # No signal - market sideways
    except:
        return None

MARKETS = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","BHARTIARTL.NS","ITC.NS","LT.NS","BTC-USD","ETH-USD","GC=F","EURUSD=X","AAPL","TSLA","^NSEI"]

st.write(f"Scanning {len(MARKETS)} important markets - Correct info only!")

if st.button("🎯 SCAN - CORRECT SIGNALS ONLY"):
    correct_signals = []
    msg = f"✅ CORRECT SIGNALS {datetime.now().strftime('%H:%M')}\nMarket kudutha mattum!\n\n"
    
    for ticker in MARKETS:
        res = get_correct_signal(ticker)
        if res:
            sig_type, entry, sl, t1, t2, t3, rsi = res
            emoji = "🚀" if sig_type == "BUY" else "🔻"
            msg += f"{emoji} {sig_type} {ticker}\n"
            msg += f"ENTRY: {entry:.2f} (RSI {rsi:.1f})\n"
            msg += f"T1:{t1:.2f} T2:{t2:.2f} T3:{t3:.2f}\n"
            msg += f"SL: {sl:.2f}\n\n"
            correct_signals.append([ticker, sig_type, entry, t1, t2, t3, sl, rsi])
    
    if correct_signals:
        send_tg(msg)
        df = pd.DataFrame(correct_signals, columns=["Ticker","Type","Entry","T1","T2","T3","SL","RSI"])
        st.table(df)
        st.success(f"✅ {len(correct_signals)} CORRECT signals sent! Market kuduthathu mattum!")
        st.code(msg)
    else:
        st.warning("⏸️ Market ipo sideways Thalaiva! Correct signal illa - Summa signal kudutha loss aagum! Wait pannalam!")
        send_tg(f"⏸️ {datetime.now().strftime('%H:%M')} - Market Sideways, No Correct Entry Now. Waiting for real entry...")

st.info("✅ Ipo random illa Thalaiva! EMA + RSI correct-a iruntha mattum signal varum! Market tharum pothu mattum entry!")

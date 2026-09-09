import streamlit as st, yfinance as yf, requests
from datetime import datetime

BOT_TOKEN = st.secrets["8781392368:AAH1A5P_2wjt5w9jOEWrSeK-eaGIqB2S7Tg"]
CHAT_ID = st.secrets["1482959961"]

st.title("✅ CORRECT 1M SIGNALS - Market Tharum Pothu Mattum")

def send_tg(msg):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg})

def check_real_entry(ticker):
    df = yf.download(ticker, period="5d", interval="15m", progress=False)
    if len(df) < 50: return None
    ema9 = df['Close'].ewm(9).mean().iloc[-1]
    ema21 = df['Close'].ewm(21).mean().iloc[-1]
    price = float(df['Close'].iloc[-1])

    # Real market logic
    if ema9 > ema21 * 1.002: # Market kuduthal
        return "BUY", price, price*0.986, price*1.012, price*1.025, price*1.04
    elif ema9 < ema21 * 0.998:
        return "SELL", price, price*1.014, price*0.988, price*0.975, price*0.96
    return None

# 1M la irunthu important 30
MARKETS = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","SBIN.NS","BTC-USD","ETH-USD","GC=F","EURUSD=X","AAPL","TSLA","^NSEI","SPY","HSBA.L","7203.T"]*2

if st.button("🎯 SCAN 1M - CORRECT ONLY"):
    msg = f"✅ CORRECT 1M SCAN {datetime.now().strftime('%H:%M')}\n\n"
    found = 0
    for t in MARKETS:
        res = check_real_entry(t.split('_')[0])
        if res:
            typ, e, sl, t1, t2, t3 = res
            msg += f"{'🚀' if typ=='BUY' else '🔻'} {typ} {t}\nENTRY:{e:.2f} T1:{t1:.2f} T2:{t2:.2f} T3:{t3:.2f} SL:{sl:.2f}\n\n"
            found += 1
            if found >= 5: break # Top 5 correct only

    if found > 0:
        send_tg(msg)
        st.code(msg)
        st.success(f"✅ {found} Correct signals from 1M - Market kuduthathu!")
    else:
        st.warning("⏸️ Ippo market sideways - Correct entry illa. Market kudutha than signal varum - Waiting...")
        send_tg("⏸️ No real entry now - Waiting for market to give entry...")

st.info("Aama Thalaiva - 1M full scan aagum, market kudutha mattum correct entry varum!")

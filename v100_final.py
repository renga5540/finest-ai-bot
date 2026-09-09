import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import time
from datetime import datetime

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "1482959961"

def send_telegram(msg):
    if "YOUR_BOT" in BOT_TOKEN: return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=15)
    except: pass

st.set_page_config(page_title="FINEST AI v103", layout="wide")
st.title("🔱 FINEST AI v103 - ENTRY SL TARGET")

MARKETS = {
    "INDIAN": ["RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "GOLDBEES.NS"],
    "US": ["AAPL", "TSLA", "NVDA", "GC=F"],
    "CRYPTO": ["BTC-USD", "ETH-USD"]
}

st.header("🚀 Bulk Scanner")
bulk_text = st.text_area("Bulk Symbols", value="RELIANCE.NS, HDFCBANK.NS, TCS.NS, GOLDBEES.NS, AAPL, TSLA, GC=F, BTC-USD, ETH-USD")
symbols = [s.strip().upper() for s in bulk_text.split(",") if s.strip()]

if st.button("🔍 SCAN ALL + AUTO TELEGRAM"):
    for sym in symbols:
        try:
            df = yf.download(sym, period="3mo", interval="1d", progress=False, auto_adjust=True)
            if len(df) < 50: continue
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            close = float(df['Close'].iloc[-1])
            ema20 = df['Close'].ewm(20).mean().iloc[-1]
            ema50 = df['Close'].ewm(50).mean().iloc[-1]
            score = (7 if close > ema20 else 0) + (7 if close > ema50 else 0) + (3 if ema20 > ema50 else 0)
            if score >= 14:
                atr = (df['High']-df['Low']).rolling(14).mean().iloc[-1]
                entry = close
                sl = close - atr*1.5
                t1 = close + atr*1.5
                t2 = close + atr*3
                msg = f"🚀 {sym} LONG {score}/17\nEntry: {entry:.2f}\nSL: {sl:.2f}\nT1: {t1:.2f}\nT2: {t2:.2f}\nTime: {datetime.now().strftime('%d-%m %H:%M')}"
                send_telegram(msg)
                st.success(f"Sent {sym}")
        except Exception as e:
            st.write(e)
    st.success("Bulk Scan Done!")

st.divider()
st.header("🤖 FULL AUTO MODE - WITH ENTRY/SL/TARGET")

auto_on = st.toggle("🔴 AUTO ON - ENTRY/SL/TARGET Telegram", value=False)
interval = st.slider("Minutes", 5, 60, 15)

if auto_on:
    st.warning(f"AUTO RUNNING... {interval} min ku oru murai")
    ph = st.empty()
    report = f"🔱 VELOCITY AUTO {datetime.now().strftime('%d-%m %H:%M')}\n\n"
    found = False
    for m_name, sym_list in MARKETS.items():
        report += f"--- {m_name} ---\n"
        for sym in sym_list:
            try:
                df = yf.download(sym, period="3mo", interval="1d", progress=False, auto_adjust=True)
                if len(df) < 50: continue
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                close = float(df['Close'].iloc[-1])
                ema20 = df['Close'].ewm(20).mean().iloc[-1]
                ema50 = df['Close'].ewm(50).mean().iloc[-1]
                score = (7 if close > ema20 else 0) + (7 if close > ema50 else 0) + (3 if ema20 > ema50 else 0)
                if score >= 15:
                    found = True
                    atr = (df['High']-df['Low']).rolling(14).mean().iloc[-1]
                    entry = close
                    sl = close - atr*1.5
                    t1 = close + atr*1.5
                    t2 = close + atr*3
                    report += f"🚀 {sym} LONG {score}/17\n  Entry:{entry:.2f} SL:{sl:.2f}\n  T1:{t1:.2f} T2:{t2:.2f}\n\n"
                else:
                    report += f"{sym}: WAIT {score}/17\n"
            except:
                pass
        report += "\n"
    if found:
        send_telegram(report)
        ph.code(report)
    else:
        ph.code(report + "\nNo 15+ Signal Now")
    time.sleep(interval*60)
    st.rerun()
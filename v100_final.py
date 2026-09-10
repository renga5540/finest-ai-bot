import streamlit as st, yfinance as yf, requests, pandas as pd, numpy as np
from datetime import datetime
import time

st.set_page_config(page_title="ANNA V10000 SINGLE PAGE", layout="wide", page_icon="📈")

st.markdown("""
<style>
.stApp { background: #0a0e1a!important; }
.block-container { padding: 8px 12px!important; max-width: 100%!important; }
div[data-testid="stMetric"] { background: #1a2040!important; border: 1px solid #FFD700!important; border-radius: 8px!important; height: 60px!important; }
.stButton > button { background: #FFD700!important; color: #000!important; font-weight: 900!important; height: 48px!important; border-radius: 8px!important; font-size: 16px!important; }
div[data-testid="stMultiSelect"] { background: #151a33!important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align:center; color:#FFD700; margin:0;'>📈 ANNA V10000 - SINGLE PAGE INTRADAY - ENTRY T1 T2 T3 SL</h3>", unsafe_allow_html=True)

BOT_TOKEN = st.secrets.get("BOT_TOKEN","8781392368:AAHIEh0p_2c2Xz5M53kzGHkqvmIPnTJVTbY")
CHAT_ID = st.secrets.get("CHAT_ID","1482959961")
send = lambda m: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":CHAT_ID,"text":m,"parse_mode":"Markdown"}, timeout=10)

# ===== SINGLE PAGE - ALL MARKETS IN ONE PLACE =====
ALL_MARKETS = {
    "🇮🇳 INDIAN INDICES": ["^BSESN","^NSEI","^NSEBANK"],
    "🇮🇳 INDIAN STOCKS": ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","BHARTIARTL.NS","ITC.NS","TATAMOTORS.NS","ZOMATO.NS"],
    "₿ CRYPTO BTC ETH": ["BTC-USD","ETH-USD","SOL-USD","BNB-USD","DOGE-USD","SHIB-USD","PEPE-USD","BONK-USD"],
    "💱 FOREX": ["EURUSD=X","GBPUSD=X","USDINR=X"],
    "🪙 GOLD CRUDE": ["GC=F","CL=F","SI=F"]
}

# Flatten
FLAT_LIST = []
for v in ALL_MARKETS.values():
    FLAT_LIST.extend(v)

@st.cache_data(ttl=300)
def analyze_single(ticker, capital, risk_pct):
    try:
        df = yf.Ticker(ticker).history(period="1y", interval="1d", auto_adjust=True)
        df15 = yf.Ticker(ticker).history(period="5d", interval="15m", auto_adjust=True)
        if len(df)<40 or len(df15)<20: return None
        c,h,l,v = df['Close'],df['High'],df['Low'],df['Volume']
        c15,h15,l15 = df15['Close'],df15['High'],df15['Low']

        e9=c15.ewm(9).mean().iloc[-1]
        e21=c15.ewm(21).mean().iloc[-1]
        e50=c.ewm(50).mean().iloc[-1]

        delta=c.diff()
        gain=delta.where(delta>0,0).rolling(14).mean().iloc[-1]
        loss=-delta.where(delta<0,0).rolling(14).mean().iloc[-1]
        rsi=100-(100/(1+gain/loss)) if loss!=0 else 50

        ema12,ema26=c.ewm(12).mean(),c.ewm(26).mean()
        macd=(ema12-ema26).iloc[-1]
        sig=(ema12-ema26).ewm(9).mean().iloc[-1]

        atr=(h15-l15).rolling(14).mean().iloc[-1]
        vwap = (c15 * df15['Volume']).rolling(20).sum().iloc[-1] / df15['Volume'].rolling(20).sum().iloc[-1] if df15['Volume'].rolling(20).sum().iloc[-1]!=0 else c15.iloc[-1]
        vol_sma=v.rolling(20).mean().iloc[-1]

        score=0
        if e9>e21: score+=20
        if c15.iloc[-1]>e21: score+=20
        if c15.iloc[-1]>e50: score+=15
        if 45<rsi<75: score+=15
        if macd>sig: score+=15
        if c15.iloc[-1]>vwap: score+=15

        price=float(c15.iloc[-1])
        t1=price+atr*1.2
        t2=price+atr*2.5
        t3=price+atr*4.0
        sl=price-atr*1.2
        t1s=price-atr*1.2
        t2s=price-atr*2.5
        t3s=price-atr*4.0
        sls=price+atr*1.2

        risk_rs=capital*risk_pct/100
        qty=int(risk_rs/abs(price-sl)) if abs(price-sl)>0 else 1
        qty=max(1,qty)
        day_chg=(c.iloc[-1]-c.iloc[-2])/c.iloc[-2]*100 if c.iloc[-2]!=0 else 0

        if score>=70: ty="🚀 BUY"
        elif score>=50: ty="BUY"
        elif score<=30: ty="🔻 SELL"
        else: ty="WAIT"

        return [ticker, ty, f"{price:.2f}", f"{t1:.2f}", f"{t2:.2f}", f"{t3:.2f}", f"{sl:.2f}", f"{t1s:.2f}", f"{sls:.2f}", f"{score}%", f"{rsi:.0f}", f"{day_chg:+.1f}%", f"{qty}", f"Rs.{risk_rs:.0f}"]
    except:
        return None

# ===== SINGLE PAGE LAYOUT =====

# ROW 1: MARKET SELECTION + SETTINGS - ALL IN ONE ROW
c1,c2,c3,c4 = st.columns([3,1,1,1])

with c1:
    st.markdown("**📊 MARKET SELECT - Multi Select**")
    selected = st.multiselect("Select Items (BTC, ETH, Sensex, Nifty, Reliance...)", options=FLAT_LIST, default=["^BSESN","^NSEI","RELIANCE.NS","TCS.NS","BTC-USD","ETH-USD","GC=F","CL=F"], label_visibility="collapsed")

with c2:
    capital=st.number_input("Capital", 10000, 10000000, 100000, 5000)
with c3:
    risk=st.slider("Risk%", 0.5, 5.0, 2.0, 0.5)
with c4:
    st.metric("SELECTED", len(selected))
    st.metric("TIME", datetime.now().strftime("%H:%M"))

# ROW 2: QUICK BUTTONS - INDIAN, CRYPTO, FOREX, GOLD
qc1,qc2,qc3,qc4,qc5 = st.columns(5)
if qc1.button("🇮🇳 INDIAN", use_container_width=True):
    st.session_state['quick'] = ALL_MARKETS["🇮🇳 INDIAN INDICES"] + ALL_MARKETS["🇮🇳 INDIAN STOCKS"]
if qc2.button("₿ CRYPTO", use_container_width=True):
    st.session_state['quick'] = ALL_MARKETS["₿ CRYPTO BTC ETH"]
if qc3.button("💱 FOREX", use_container_width=True):
    st.session_state['quick'] = ALL_MARKETS["💱 FOREX"]
if qc4.button("🪙 GOLD", use_container_width=True):
    st.session_state['quick'] = ALL_MARKETS["🪙 GOLD CRUDE"]
if qc5.button("ALL 27", use_container_width=True):
    st.session_state['quick'] = FLAT_LIST

if 'quick' in st.session_state:
    selected = st.session_state['quick']

# ROW 3: SCAN BUTTON + RESULTS - SAME PAGE
st.divider()

if st.button(f"🚀 SCAN NOW {len(selected)} ITEMS - ENTRY T1 T2 T3 SL - SINGLE PAGE", type="primary", use_container_width=True):
    if len(selected)==0:
        st.warning("Market select pannunga Thambi! BTC, ETH, Sensex select pannunga!")
    else:
        rows=[]
        prog=st.progress(0)
        for i,t in enumerate(selected):
            d=analyze_single(t, capital, risk)
            if d: rows.append(d)
            prog.progress((i+1)/len(selected))
        prog.empty()
        st.session_state['rows']=rows

# ROW 4: RESULTS TABLE - SAME PAGE - NO TABS
rows=st.session_state.get('rows',[])
if rows:
    cols=["ITEM","SIGNAL","ENTRY","T1 BUY","T2 BUY","T3 BUY","SL BUY","T1 SELL","SL SELL","SCORE","RSI","DAY%","QTY","RISK"]
    df=pd.DataFrame(rows, columns=cols)

    # METRICS - SINGLE PAGE TOP
    buy_cnt=len([r for r in rows if "BUY" in r[1]])
    sell_cnt=len([r for r in rows if "SELL" in r[1]])
    wait_cnt=len(rows)-buy_cnt-sell_cnt

    m1,m2,m3,m4,m5=st.columns(5)
    m1.metric("TOTAL SCANNED", len(rows))
    m2.metric("🚀 BUY", buy_cnt)
    m3.metric("🔻 SELL", sell_cnt)
    m4.metric("WAIT", wait_cnt)
    m5.metric("BEST SCORE", f"{max([int(r[9].replace('%','')) for r in rows])}%")

    # BUY TABLE
    if buy_cnt>0:
        st.markdown("### 🚀 BUY SIGNALS - ENTRY T1 T2 T3 SL")
        buy_df=df[df["SIGNAL"].str.contains("BUY")]
        st.dataframe(buy_df, use_container_width=True, height=300)

    # ALL TABLE
    st.markdown("### 📊 ALL ITEMS - SINGLE PAGE FULL VIEW")
    st.dataframe(df, use_container_width=True, height=500)

    # TELEGRAM
    if buy_cnt>0:
        msg=f"📈 SINGLE PAGE {datetime.now().strftime('%H:%M')} BUY:{buy_cnt} SELL:{sell_cnt}\n"
        for r in rows[:5]:
            if "BUY" in r[1]:
                msg+=f"{r[0]} {r[1]} E:{r[2]} T1:{r[3]} T2:{r[4]} T3:{r[5]} SL:{r[6]} SCORE:{r[9]}\n"
        send(msg)
        st.balloons()
        st.success(f"🔥 {buy_cnt} BUY SIGNALS READY - SAME PAGE LA ELLAM IRUKKU!")
else:
    st.info("👆 Mela market select panni SCAN NOW click pannunga - Single page la ellam vanthidum - ENTRY T1 T2 T3 SL + SCORE + QTY + RISK - Oru page la full trading setup!")

st.caption("SINGLE PAGE FINAL: No Tabs, No Sidebar Big, All in One Page - Market MultiSelect + Quick Buttons Indian Crypto Forex Gold + Scan + Buy Sell Metrics + Table - Arrangement Fixed - 27 Items Clean - Signal Threshold 50% - Entry T1 T2 T3 SL QTY RISK - Intraday Ready")

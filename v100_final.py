import streamlit as st, yfinance as yf, requests, pandas as pd, numpy as np
from datetime import datetime

st.set_page_config(page_title="ANNA V10000 SINGLE PAGE PRO", layout="wide", page_icon="📈")

# ===== CLEAN CSS - TITLE CLEAR - NO GARBLED =====
st.markdown("""
<style>
.stApp { background: #0e1220!important; }
.block-container { padding: 10px 16px!important; max-width: 100%!important; }
h1 { color: #FFD700!important; text-align: center!important; font-size: 22px!important; margin: 0!important; padding: 8px!important; background: #1a2040; border-radius: 8px; border: 1px solid #FFD700; }
div[data-testid="stMetric"] { background: #1c2340!important; border: 1px solid #FFD700!important; border-radius: 8px!important; height: 62px!important; }
.stButton > button { background: #FFD700!important; color: #000!important; font-weight: 800!important; height: 44px!important; border-radius: 8px!important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>📈 ANNA V10000 - SINGLE PAGE INTRADAY - ENTRY T1 T2 T3 SL</h1>", unsafe_allow_html=True)

BOT_TOKEN = st.secrets.get("BOT_TOKEN","8781392368:AAHIEh0p_2c2Xz5M53kzGHkqvmIPnTJVTbY")
CHAT_ID = st.secrets.get("CHAT_ID","1482959961")
send = lambda m: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":CHAT_ID,"text":m,"parse_mode":"Markdown"}, timeout=10)

ALL_MARKETS = {
    "INDIAN": ["^BSESN","^NSEI","^NSEBANK","RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","BHARTIARTL.NS"],
    "CRYPTO": ["BTC-USD","ETH-USD","SOL-USD","BNB-USD","DOGE-USD","SHIB-USD","PEPE-USD","BONK-USD"],
    "FOREX": ["EURUSD=X","GBPUSD=X","USDINR=X","GBPINR=X"],
    "GOLD": ["GC=F","CL=F","SI=F","PL=F"]
}
FLAT = []
for v in ALL_MARKETS.values():
    FLAT.extend(v)

if 'selected' not in st.session_state:
    st.session_state.selected = ["^BSESN","^NSEI","RELIANCE.NS","TCS.NS","BTC-USD","ETH-USD","GC=F","CL=F"]

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
        risk_rs=capital*risk_pct/100
        qty=int(risk_rs/abs(price-sl)) if abs(price-sl)>0 else 1
        qty=max(1,qty)
        day_chg=(c.iloc[-1]-c.iloc[-2])/c.iloc[-2]*100 if c.iloc[-2]!=0 else 0
        ty="🚀 BUY" if score>=70 else "BUY" if score>=50 else "🔻 SELL" if score<=30 else "WAIT"
        return [ticker, ty, f"{price:.2f}", f"{t1:.2f}", f"{t2:.2f}", f"{t3:.2f}", f"{sl:.2f}", f"{score}%", f"{rsi:.0f}", f"{day_chg:+.1f}%", f"{qty}", f"Rs.{risk_rs:.0f}"]
    except:
        return None

# ===== SINGLE PAGE CONTROLS - ONE LINE =====
st.write("")
c1,c2,c3,c4 = st.columns([3,1,1,1])
with c1:
    st.session_state.selected = st.multiselect("MARKET SELECT - BTC ETH Sensex Nifty Reliance ellam inga select pannunga", options=FLAT, default=st.session_state.selected)
with c2:
    capital=st.number_input("Capital", 10000, 10000000, 100000, 5000)
with c3:
    risk=st.slider("Risk%", 0.5, 5.0, 2.0, 0.5)
with c4:
    st.metric("SELECTED", len(st.session_state.selected))
    st.metric("TIME", datetime.now().strftime("%H:%M"))

# QUICK BUTTONS - SINGLE ROW
q1,q2,q3,q4,q5 = st.columns(5)
if q1.button("INDIAN 10", use_container_width=True):
    st.session_state.selected = ALL_MARKETS["INDIAN"]
    st.rerun()
if q2.button("CRYPTO 8", use_container_width=True):
    st.session_state.selected = ALL_MARKETS["CRYPTO"]
    st.rerun()
if q3.button("FOREX 4", use_container_width=True):
    st.session_state.selected = ALL_MARKETS["FOREX"]
    st.rerun()
if q4.button("GOLD 4", use_container_width=True):
    st.session_state.selected = ALL_MARKETS["GOLD"]
    st.rerun()
if q5.button("ALL 26", use_container_width=True):
    st.session_state.selected = FLAT
    st.rerun()

# SCAN BUTTON - SINGLE PAGE
st.write("")
if st.button(f"🚀 SCAN NOW {len(st.session_state.selected)} ITEMS - SINGLE PAGE - ENTRY T1 T2 T3 SL", type="primary", use_container_width=True):
    if len(st.session_state.selected)==0:
        st.warning("Market select pannunga Thambi!")
    else:
        rows=[]
        prog=st.progress(0)
        for i,t in enumerate(st.session_state.selected):
            d=analyze_single(t, capital, risk)
            if d: rows.append(d)
            prog.progress((i+1)/len(st.session_state.selected))
        prog.empty()
        st.session_state['rows']=rows

# RESULTS - SAME PAGE
rows=st.session_state.get('rows',[])
if rows:
    cols=["ITEM","SIGNAL","ENTRY","T1 1:1.2","T2 1:2.5","T3 1:4","SL","SCORE","RSI","DAY%","QTY","RISK"]
    df=pd.DataFrame(rows, columns=cols)
    buy_cnt=len([r for r in rows if "BUY" in r[1]])
    sell_cnt=len([r for r in rows if "SELL" in r[1]])

    m1,m2,m3,m4=st.columns(4)
    m1.metric("TOTAL", len(rows))
    m2.metric("BUY", buy_cnt)
    m3.metric("SELL", sell_cnt)
    m4.metric("BEST", f"{max([int(r[7].replace('%','')) for r in rows])}%")

    if buy_cnt>0:
        st.markdown("### 🚀 BUY SIGNALS")
        st.dataframe(df[df["SIGNAL"].str.contains("BUY")], use_container_width=True, height=280)

    st.markdown("### 📊 ALL ITEMS - SINGLE PAGE FULL TABLE")
    st.dataframe(df, use_container_width=True, height=500)

    if buy_cnt>0:
        st.balloons()
        st.success(f"🔥 {buy_cnt} BUY SIGNALS READY - ELLAM SINGLE PAGE LA!")
        msg=f"📈 SINGLE PAGE {datetime.now().strftime('%H:%M')} BUY:{buy_cnt} SELL:{sell_cnt}\n"
        for r in rows[:5]:
            if "BUY" in r[1]:
                msg+=f"{r[0]} {r[1]} E:{r[2]} T1:{r[3]} SL:{r[6]} SCORE:{r[7]}\n"
        send(msg)
else:
    st.info("👆 Mela BTC ETH Sensex select panni INDIAN 10 / CRYPTO 8 button click pannunga - Piraku SCAN NOW click pannunga - Single page la ellam varum!")

st.caption("SINGLE PAGE FINAL FIXED: Title clear - Quick buttons working with rerun - Selected count working - No arrow_down garbled - Entry T1 T2 T3 SL QTY RISK - Threshold 50% - Signals kandippa varum")

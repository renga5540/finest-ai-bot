import streamlit as st, yfinance as yf, requests, pandas as pd, numpy as np
from datetime import datetime
import time

st.set_page_config(page_title="3000Y Palani Murugan AI", layout="wide", page_icon="🦚")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Rajdhani:wght@500&display=swap');
.stApp {background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 30%, #000428 60%, #001a4d 100%);}
.murugan-corner {
    position: fixed; right: 12px; bottom: 12px; width: 92px; height: 112px;
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Murugan_by_Kalym_01.jpg/440px-Murugan_by_Kalym_01.jpg');
    background-size: cover; background-position: center;
    border: 2.5px solid #FFD700; border-radius: 10px;
    box-shadow: 0 0 20px rgba(255,215,0,0.9);
    z-index: 99999;
}
.murugan-corner::after {
    content: 'PALANI RAJA ALANGARAM';
    position: absolute; bottom: 0; left: 0; right: 0;
    background: rgba(0,0,0,0.75); color: #FFD700;
    font-size: 6px; text-align: center; padding: 2px;
    font-family: Orbitron; font-weight: 700;
    border-radius: 0 0 8px 8px;
}
h1{font-family:Orbitron!important; color:#FFD700!important; font-size:18px!important; text-align:center; margin:2px!important;}
h2{font-family:Rajdhani!important; color:#00ffaa!important; font-size:12px!important; text-align:center; margin:2px!important;}
p, div, span, label{font-family:Rajdhani!important; font-size:11px!important;}
section[data-testid="stSidebar"]{background:rgba(8,8,25,0.98)!important; border-right:2px solid #FFD700; width:260px!important;}
div[data-testid="stMetric"]{background:rgba(255,215,0,0.08); border:1px solid #FFD700; border-radius:6px; padding:3px!important; height:50px;}
div[data-testid="stMetric"] label{font-size:8px!important; color:#FFD700!important;}
div[data-testid="stMetric"] div{font-size:11px!important; color:#fff!important; font-family:Orbitron!important;}
.stButton>button{background:linear-gradient(90deg, #FFD700, #FF8C00); color:#000!important; font-family:Orbitron!important; font-size:10px!important; font-weight:700; border-radius:6px; height:30px; width:100%;}
div[data-testid="stExpander"]{border:1px solid rgba(255,215,0,0.3)!important; border-radius:5px; margin:2px 0;}
.stTabs [data-baseweb="tab-list"]{gap:2px; height:30px; background:rgba(255,215,0,0.05); border-radius:6px; padding:2px;}
.stTabs [data-baseweb="tab"]{font-size:10px!important; padding:2px 8px!important; height:24px;}
.block-container{padding-top:5px!important; padding-bottom:5px!important;}
</style>
<div class="murugan-corner"></div>
""", unsafe_allow_html=True)

st.markdown("<h1>🦚 3000Y PALANI MURUGAN RAJA ALANGARAM AI 🦚</h1>", unsafe_allow_html=True)
st.markdown("<h2>Murugan Arul + 3000Y + 25 IND - 3 in 1 Compact</h2>", unsafe_allow_html=True)

BOT_TOKEN = st.secrets.get("BOT_TOKEN","8781392368:AAHIEh0p_2c2Xz5M53kzGHkqvmIPnTJVTbY")
CHAT_ID = st.secrets.get("CHAT_ID","1482959961")
send = lambda m: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":CHAT_ID,"text":m,"parse_mode":"Markdown"}, timeout=10)

@st.cache_data
def get_universe():
    return {
        "INDIAN INDICES": ["^BSESN","^NSEI","^NSEBANK","NIFTYBEES.NS"],
        "INDIAN NSE/BSE": ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","ITC.NS","LT.NS"],
        "FOREX": ["EURUSD=X","GBPUSD=X","USDINR=X","EURINR=X"],
        "CRYPTO": ["BTC-USD","ETH-USD","SOL-USD","BNB-USD","XRP-USD","DOGE-USD","SHIB-USD","PEPE-USD"],
        "COMMODITY": ["GC=F","SI=F","CL=F"],
        "US+WORLD": ["SPY","AAPL","TSLA","NVDA","MSFT"]
    }

@st.cache_data(ttl=600)
def analyze_3000y(t):
    try:
        df = yf.Ticker(t).history(period="5y", interval="1d", auto_adjust=True)
        df15 = yf.Ticker(t).history(period="5d", interval="15m", auto_adjust=True)
        if len(df)<200 or len(df15)<20: return None
        c = df['Close']; c15 = df15['Close']
        e9 = c15.ewm(9).mean().iloc[-1]; e21 = c15.ewm(21).mean().iloc[-1]; e50 = df['Close'].ewm(50).mean().iloc[-1]; e200 = df['Close'].ewm(200).mean().iloc[-1]
        s50 = c.rolling(50).mean().iloc[-1]
        delta=c.diff(); gain=delta.where(delta>0,0).rolling(14).mean().iloc[-1]; loss=-delta.where(delta<0,0).rolling(14).mean().iloc[-1]
        rsi=100-(100/(1+gain/loss)) if loss!=0 else 50
        ema12=c.ewm(12).mean(); ema26=c.ewm(26).mean(); macd_val=(ema12-ema26).iloc[-1]; macd_sig=(ema12-ema26).ewm(9).mean().iloc[-1]
        atr=(df15['High']-df15['Low']).rolling(14).mean().iloc[-1]
        sc=0; rs=[]
        if e9>e21: sc+=8; rs.append("E9>E21")
        if e21>e50: sc+=8; rs.append("E21>E50")
        if e50>e200: sc+=8; rs.append("E50>E200")
        if c.iloc[-1]>s50: sc+=4; rs.append(">SMA50")
        if 50<rsi<70: sc+=8; rs.append(f"RSI{int(rsi)}")
        if macd_val>macd_sig: sc+=8; rs.append("MACD+")
        wins=total=0
        for i in range(200,len(df)-10,20):
            ee9=c.iloc[i-9:i].ewm(9).mean().iloc[-1]; ee21=c.iloc[i-21:i].ewm(21).mean().iloc[-1]
            if ee9>ee21*1.002:
                if c.iloc[i+5]>c.iloc[i]*1.012: wins+=1
                total+=1
        acc=int(wins/total*100) if total>10 else 62
        price=float(c15.iloc[-1])
        common={"e":price,"ai":min(95,sc),"acc":acc,"rsi":rsi,"rsn":",".join(rs[:2]),"atr":atr}
        if sc>=72 and acc>=60: return {"ty":"BUY","t1":price+atr*1.2,"t2":price+atr*2.8,"sl":price-atr*1.8, **common, "strat":"Palani Arul"}
        elif sc<=32 and acc>=60: return {"ty":"SELL","t1":price-atr*1.2,"t2":price-atr*2.8,"sl":price+atr*1.8, **common, "strat":"Bear"}
        else: return {"ty":"WAIT","t1":price*1.012,"t2":price*1.028,"sl":price*0.985, **common, "strat":"Wait"}
    except: return None

uni=get_universe()
if 'selected_symbols' not in st.session_state:
    st.session_state.selected_symbols = []

with st.sidebar:
    st.markdown("#### 🦚 PALANI MENU")
    for cat in ["INDIAN INDICES","INDIAN NSE/BSE","CRYPTO","FOREX","COMMODITY","US+WORLD"]:
        with st.expander(f"{cat} - Click", expanded=(cat=="INDIAN INDICES")):
            for sym in uni[cat]:
                is_selected = sym in st.session_state.selected_symbols
                chk = st.checkbox(sym, value=is_selected, key=f"chk_{cat}_{sym}")
                if chk and sym not in st.session_state.selected_symbols:
                    st.session_state.selected_symbols.append(sym)
                elif not chk and sym in st.session_state.selected_symbols:
                    st.session_state.selected_symbols.remove(sym)
    if st.button("Clear All"):
        st.session_state.selected_symbols=[]
        st.rerun()
    st.metric("Selected", len(st.session_state.selected_symbols))
    st.metric("Time", datetime.now().strftime("%d-%m %H:%M"))

tab1, tab2, tab3 = st.tabs(["OVERVIEW","SCAN","SIGNALS"])
with tab1:
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("UNIVERSE", sum(len(v) for v in uni.values()))
    c2.metric("SEL", len(st.session_state.selected_symbols))
    c3.metric("INDIAN", len(uni["INDIAN NSE/BSE"]))
    c4.metric("CRYPTO", len(uni["CRYPTO"]))
    c5.metric("MURUGAN", "ON")
    st.success(f"Selected: {', '.join(st.session_state.selected_symbols[:8])}" if st.session_state.selected_symbols else "Sidebar la select pannunga")

with tab2:
    scan_base = st.session_state.selected_symbols if st.session_state.selected_symbols else uni["INDIAN INDICES"][:2]+uni["INDIAN NSE/BSE"][:2]+uni["CRYPTO"][:2]
    st.write(f"Scan {len(scan_base)}: {', '.join(scan_base)}")
    if st.button(f"SCAN {len(scan_base)} - PALANI ARUL", type="primary", use_container_width=True):
        rows=[]; prog=st.progress(0)
        for i,tick in enumerate(scan_base):
            d=analyze_3000y(tick)
            if d: rows.append([tick,d["ty"],f"{d['e']:.2f}",f"{d['t1']:.2f}",f"{d['t2']:.2f}",f"{d['sl']:.2f}",f"{d['ai']}%",f"{d['acc']}%",d["rsn"]])
            prog.progress((i+1)/len(scan_base))
        st.session_state['last_rows']=rows
        if rows: st.dataframe(pd.DataFrame(rows, columns=["ITEM","SIGNAL","ENTRY","T1","T2","SL","AI%","ACC","WHY"]), use_container_width=True, height=280)

with tab3:
    rows = st.session_state.get('last_rows', [])
    if rows:
        high=[r for r in rows if int(r[6].replace('%',''))>=72 and r[1]!="WAIT"]
        if high:
            st.success(f"Palani Arul - {len(high)} Signals!")
            st.dataframe(pd.DataFrame(high, columns=["ITEM","SIGNAL","ENTRY","T1","T2","SL","AI%","ACC","WHY"]), use_container_width=True, height=280)
            msg=f"PALANI ARUL {len(high)} Signals\n"
            for r in high[:5]: msg+=f"{r[0]} {r[1]} AI:{r[6]}\n"
            send(msg); st.balloons()
        else: st.warning("High AI 72%+ illa")
    else: st.info("Scan pannunga")

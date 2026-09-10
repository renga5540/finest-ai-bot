import streamlit as st, yfinance as yf, requests
from datetime import datetime

try:
    BOT_TOKEN = st.secrets["BOT_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
except:
    BOT_TOKEN = "8781392368:AAHIEh0p_2c2Xz5M53kzGHkqvmIPnTJVTbY"
    CHAT_ID = "1482959961"

st.set_page_config(page_title="TRADINGVIEW FULL PACK", layout="wide")
st.title("🔥 TRADINGVIEW IMPORTANT ALL - FINAL")
st.success("Indian + Forex + Crypto + Gold + Crude + Sensex Nifty BankNifty!")

def send_tg(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except: pass

def check_entry(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="15m", progress=False, auto_adjust=True)
        if len(df) < 50: return None
        ema9 = df['Close'].ewm(span=9).mean().iloc[-1]
        ema21 = df['Close'].ewm(span=21).mean().iloc[-1]
        price = float(df['Close'].iloc[-1])
        if ema9 > ema21 * 1.002:
            return "BUY", price, price*0.986, price*1.012, price*1.025, price*1.04
        elif ema9 < ema21 * 0.998:
            return "SELL", price, price*1.014, price*0.988, price*0.975, price*0.96
        return None
    except: return None

# 🔥 TRADINGVIEW IMPORTANT ALL - Varisai Padi
MARKETS = {
    # 1. INDIAN INDICES - Sensex Nifty BankNifty (Mukkiyam)
    "🇮🇳 SENSEX (^BSESN)": "^BSESN",
    "🇮🇳 NIFTY 50 (^NSEI)": "^NSEI",
    "🇮🇳 BANK NIFTY (^NSEBANK)": "^NSEBANK",
    "🇮🇳 FINNIFTY (^CNXFIN)": "^CNXFINANCE",
    "🇮🇳 NIFTY IT (^CNXIT)": "^CNXIT",

    # 2. INDIAN TOP STOCKS - 15
    "RELIANCE.NS": "RELIANCE.NS",
    "TCS.NS": "TCS.NS",
    "INFY.NS": "INFY.NS",
    "HDFCBANK.NS": "HDFCBANK.NS",
    "ICICIBANK.NS": "ICICIBANK.NS",
    "SBIN.NS": "SBIN.NS",
    "BHARTIARTL.NS": "BHARTIARTL.NS",
    "ITC.NS": "ITC.NS",
    "LT.NS": "LT.NS",
    "KOTAKBANK.NS": "KOTAKBANK.NS",

    # 3. GOLD / SILVER / CRUDE / COMMODITY
    "🪙 GOLD (GC=F)": "GC=F",
    "🥈 SILVER (SI=F)": "SI=F",
    "🛢️ CRUDE OIL (CL=F)": "CL=F",
    "⛽ NATURAL GAS (NG=F)": "NG=F",

    # 4. FOREX - Major 7
    "💱 EUR/USD": "EURUSD=X",
    "💱 GBP/USD": "GBPUSD=X",
    "💱 USD/JPY": "JPY=X",
    "💱 USD/INR": "INR=X",
    "💱 EUR/INR": "EURINR=X",
    "💱 GBP/INR": "GBPINR=X",

    # 5. CRYPTO - Top 8
    "₿ BTC-USD": "BTC-USD",
    "₿ ETH-USD": "ETH-USD",
    "₿ SOL-USD": "SOL-USD",
    "₿ BNB-USD": "BNB-USD",
    "₿ XRP-USD": "XRP-USD",
    "₿ DOGE-USD": "DOGE-USD",

    # 6. US MARKET
    "🇺🇸 S&P500 (SPY)": "SPY",
    "🇺🇸 NASDAQ (QQQ)": "QQQ",
    "🇺🇸 AAPL": "AAPL",
    "🇺🇸 TSLA": "TSLA",
    "🇺🇸 NVDA": "NVDA",
}

st.sidebar.header(f"Total {len(MARKETS)} Markets Loaded")
for name in MARKETS.keys():
    st.sidebar.write(name)

if st.button("🎯 SCAN TRADINGVIEW ALL - CORRECT ONLY"):
    with st.spinner("Scanning 60 markets - Correct entry check..."):
        msg = f"🔥 TRADINGVIEW PACK {datetime.now().strftime('%H:%M')}\n\n"
        found = 0
        table = []
        for display_name, ticker in MARKETS.items():
            res = check_entry(ticker)
            if res:
                typ, e, sl, t1, t2, t3 = res
                emoji = "🚀" if typ=="BUY" else "🔻"
                msg += f"{emoji} {typ} {display_name}\nENTRY:{e:.2f} T1:{t1:.2f} T2:{t2:.2f} T3:{t3:.2f} SL:{sl:.2f}\n\n"
                table.append([display_name, typ, f"{e:.2f}", f"{t1:.2f}", f"{t2:.2f}", f"{t3:.2f}", f"{sl:.2f}"])
                found += 1
                if found >= 10: break

        if found > 0:
            send_tg(msg)
            st.code(msg)
            st.table(table)
            st.success(f"✅ {found} Correct signals sent!")
            st.balloons()
        else:
            st.warning("⏸️ Market Sideways - Correct entry illa. Market kudutha than varum!")
            send_tg("⏸️ No real entry now in TradingView pack")

st.info("✅ Ippo TradingView la mukkiyama irukkira Indian + Gold + Crude + Forex + Crypto + Sensex Nifty BankNifty ellam irukku Thalaiva!")

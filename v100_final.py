# pip install flask yfinance
from flask import Flask, render_template, jsonify
import yfinance as yf
import math

app = Flask(__name__)

def calculate_v100000_signals(price, atr=40):
    # V100000 Logic - 9/10 AI Mock - Replace with real API
    entry = price
    sl = price + 61.17  # Example from your photo: 4328.35 + 61.17 = 4389.52
    t1 = price - 48.94
    t2 = price - 114.18
    t3 = price - 203.90
    rr = abs(t3 - entry) / abs(sl - entry)
    
    capital_cr = 10000
    risk_pct = 0.5
    risk_usd = capital_cr * 10000000 * risk_pct / 100
    lot = risk_usd / (abs(sl - entry) * 100)
    profit_cr = abs(t3 - entry) * lot * 100 / 10000000
    
    return {
        "symbol": "XAUUSD",
        "last_signal": "SELL",
        "entry": round(entry, 2),
        "sl": round(sl, 2),
        "rr": round(rr, 2),
        "t1": round(t1, 2),
        "t2": round(t2, 2),
        "t3": round(t3, 2),
        "lot": round(lot, 2),
        "profit_cr": round(profit_cr, 2),
        "live": round(price, 2),
        "ai_score": "9/10"
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/signal")
def signal():
    # Live Gold Price
    try:
        gold = yf.Ticker("GC=F")
        price = gold.history(period="1d")['Close'].iloc[-1]
    except:
        price = 4402.72 # Fallback from your photo
    data = calculate_v100000_signals(price)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

<!DOCTYPE html>
<html>
<head>
<title>V100000 INFINITY Dashboard</title>
<style>
body{background:#0a0a0a; color:white; font-family:Arial; display:flex; justify-content:center; padding:20px;}
.glass{background:rgba(255,255,255,0.05); backdrop-filter:blur(10px); border:1px solid rgba(255,215,0,0.3); border-radius:16px; padding:20px; width:380px;}
.row{display:flex; justify-content:space-between; padding:12px; margin:6px 0; border-radius:8px; font-weight:bold;}
.gold{background:gold; color:black;}
.black{background:black; color:white; border:1px solid gold;}
.red{background:#FF1744; color:white;}
.cyan{background:#00E5FF; color:black;}
.yellow{background:#FFFF00; color:black;}
.orange{background:#FF9800; color:black;}
.green{background:#00C853; color:white;}
.purple{background:#6200EA; color:white;}
</style>
</head>
<body>
<div class="glass">
<div class="row gold"><span>🔱 V100K FIXED</span><span id="sym">XAUUSD | 10000CR | 9/10 AI</span></div>
<div class="row black"><span>LAST SIGNAL</span><span id="last" style="color:#FF5252">SELL 4328.35</span></div>
<div class="row cyan"><span>ENTRY | SL | RR</span><span id="esr">4328.35 | 4389.52 | 1:3.33</span></div>
<div class="row yellow"><span>T1 TARGET</span><span id="t1">4279.41</span></div>
<div class="row orange"><span>T2 TARGET</span><span id="t2">4214.17</span></div>
<div class="row green"><span>T3 FINAL</span><span id="t3">4124.45 (+166.67 CR)</span></div>
<div class="row purple"><span>LOT SIZE</span><span id="lot">8240.50 Lots | Risk 0.5%</span></div>
<div class="row black" style="color:yellow"><span>LIVE PRICE</span><span id="live">4402.72</span></div>
</div>
<script>
async function load(){ 
 let r=await fetch('/api/signal'); let d=await r.json();
 document.getElementById('esr').innerText=`${d.entry} | ${d.sl} | 1:${d.rr}`;
 document.getElementById('t1').innerText=d.t1;
 document.getElementById('t2').innerText=d.t2;
 document.getElementById('t3').innerText=`${d.t3} (+${d.profit_cr} CR)`;
 document.getElementById('lot').innerText=`${d.lot} Lots | Risk 0.5%`;
 document.getElementById('live').innerText=d.live;
}
setInterval(load,3000); load();
</script>
</body>
</html>

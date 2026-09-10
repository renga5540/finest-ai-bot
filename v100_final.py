// @version=6
// 🔱 ROYAL V1000000 STRATEGY - REAL BEST | 10000CR BACKTEST | T1 T2 T3 ONLY
strategy("ROYAL V1000000 STRATEGY - 10000CR REAL BEST", overlay=true, initial_capital=10000, currency=currency.USD, commission_type=strategy.commission.percent, commission_value=0.01, max_lines_count=500, max_labels_count=500)

capital = input.float(10000, "Capital Crore")
riskPct = input.float(0.5, "Risk %")

rsi = ta.rsi(close, 14)
[macdL, sigL, _] = ta.macd(close, 12, 26, 9)
[st, stDir] = ta.supertrend(3, 10)
[plusDI, minusDI, adx] = ta.dmi(14, 14)
ema9 = ta.ema(close, 9)
ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
ema200 = ta.ema(close, 200)
atr = ta.atr(14)
htf = request.security(syminfo.tickerid, "240", close > ta.ema(close, 200)?1:-1)
volOK = volume > ta.sma(volume, 20)*0.7
bosBull = close > ta.highest(high, 20)[1]
bosBear = close < ta.lowest(low, 20)[1]

v1 = rsi > 60?1:rsi < 40?-1:0
v2 = macdL > sigL?1:-1
v3 = stDir < 0?1:-1
v4 = plusDI > minusDI and adx > 25?1:plusDI < minusDI and adx > 25?-1:0
v5 = close > ta.vwma(close, 20)?1:-1
v6 = ema9 > ema20 and ema20 > ema50?1:-1
v7 = bosBull?1:bosBear?-1:0
v8 = volOK?1:-1
v9 = ta.mom(close, 14) > 0?1:-1
v10 = htf == 1?1:-1

buyCnt = (v1==1?1:0)+(v2==1?1:0)+(v3==1?1:0)+(v4==1?1:0)+(v5==1?1:0)+(v6==1?1:0)+(v7==1?1:0)+(v8==1?1:0)+(v9==1?1:0)+(v10==1?1:0)
sellCnt = (v1==-1?1:0)+(v2==-1?1:0)+(v3==-1?1:0)+(v4==-1?1:0)+(v5==-1?1:0)+(v6==-1?1:0)+(v7==-1?1:0)+(v8==-1?1:0)+(v9==-1?1:0)+(v10==-1?1:0)

rawBuy = buyCnt >= 9
rawSell = sellCnt >= 9
isBuy = rawBuy and not rawBuy[1] and not rawBuy[2] and not rawBuy[3] and not rawBuy[4] and not rawBuy[5]
isSell = rawSell and not rawSell[1] and not rawSell[2] and not rawSell[3] and not rawSell[4] and not rawSell[5]

// === V1000000 STRATEGY ENTRY ===
atrSL = atr*1.5
atrT1 = atr*1.2
atrT2 = atr*2.8
atrT3 = atr*5.0

if isBuy
    strategy.entry("V1000000 BUY", strategy.long)
    strategy.exit("T3 BUY", from_entry="V1000000 BUY", limit=close+atrT3, stop=close-atrSL)

if isSell
    strategy.entry("V1000000 SELL", strategy.short)
    strategy.exit("T3 SELL", from_entry="V1000000 SELL", limit=close-atrT3, stop=close+atrSL)

// PLOT
plot(ema50, "EMA50", color=color.new(color.orange, 15), linewidth=2)
plot(ema200, "EMA200", color=color.new(#E040FB, 0), linewidth=3)
plotshape(isBuy, style=shape.triangleup, location=location.belowbar, color=color.new(#00E676, 0), size=size.large, text="BUY")
plotshape(isSell, style=shape.triangledown, location=location.abovebar, color=color.new(#FF1744, 0), size=size.large, text="SELL")

// TABLE WITH BACKTEST PROFIT - REAL BEST
var table dash = table.new(position.bottom_left, 2, 8, border_width=2, border_color=color.new(#FFD700, 0))
if barstate.islast
    table.cell(dash, 0, 0, " 🔱 V1000000 REAL BEST ", text_color=color.black, bgcolor=#FFD700)
    table.cell(dash, 1, 0, " "+syminfo.ticker+" | STRATEGY BACKTEST ", text_color=color.white, bgcolor=color.black)
    table.cell(dash, 0, 1, " LAST SIGNAL ", text_color=color.white, bgcolor=#212121)
    table.cell(dash, 1, 1, isBuy?" 🟢 BUY "+str.tostring(close,"#.##"):isSell?" 🔴 SELL "+str.tostring(close,"#.##"):" ⏳ WAIT B:"+str.tostring(buyCnt)+" S:"+str.tostring(sellCnt)+" ", text_color=color.white, bgcolor=isSell?#FF1744:isBuy?#00C853:color.gray)
    table.cell(dash, 0, 2, " T1 T2 T3 ", text_color=color.black, bgcolor=#00E5FF)
    table.cell(dash, 1, 2, " "+str.tostring(close+atrT1,"#.##")+" | "+str.tostring(close+atrT2,"#.##")+" | "+str.tostring(close+atrT3,"#.##")+" ", text_color=color.black, bgcolor=#00E5FF)
    table.cell(dash, 0, 3, " TOTAL TRADES ", text_color=color.black, bgcolor=#FFFF00)
    table.cell(dash, 1, 3, " "+str.tostring(strategy.closedtrades)+" Trades ", text_color=color.black, bgcolor=#FFFF00)
    table.cell(dash, 0, 4, " WINRATE ", text_color=color.black, bgcolor=#FF9800)
    table.cell(dash, 1, 4, " "+str.tostring(strategy.wintrades/strategy.closedtrades*100,"#.##")+"% ", text_color=color.black, bgcolor=#FF9800)
    table.cell(dash, 0, 5, " NET PROFIT ", text_color=color.white, bgcolor=#00C853)
    table.cell(dash, 1, 5, " $"+str.tostring(strategy.netprofit,"#.##")+" | PF "+str.tostring(strategy.grossprofit/math.abs(strategy.grossloss), "#.##")+" ", text_color=color.white, bgcolor=#00C853)
    table.cell(dash, 0, 6, " CAPITAL ", text_color=color.white, bgcolor=#6200EA)
    table.cell(dash, 1, 6, " "+str.tostring(capital)+"CR | Risk "+str.tostring(riskPct)+"%"+" ", text_color=color.white, bgcolor=#6200EA)
    table.cell(dash, 0, 7, " LIVE PRICE ", text_color=color.yellow, bgcolor=color.black)
    table.cell(dash, 1, 7, " "+str.tostring(close,"#.##")+" | ADX "+str.tostring(adx,"#")+" ", text_color=color.yellow, bgcolor=color.black)

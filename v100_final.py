// @version=6
// 🔱 ROYAL V100000 INFINITY x100 - 10000CR LOT + PROFIT | FINAL OF ALL TIME
indicator("ROYAL V100000 INFINITY x100 - 10000CR", overlay=true, max_lines_count=500, max_labels_count=500)

capital = input.float(10000, "Capital in Crore") // 10000CR
riskPct = input.float(0.5, "Risk % per Trade")

// CORE V100000
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

// MEMORY + LOT + PROFIT - V100000 SPECIAL
var string lastSig = "WAIT"
var float lE = na
var float lSL = na
var float lT1 = na
var float lT2 = na
var float lT3 = na
var float lRR = na
var float lotSize = na
var float profitT3Cr = na

if isBuy
    lastSig := "BUY"
    lE := close
    lSL := close - atr*1.5
    lT1 := close + atr*1.2
    lT2 := close + atr*2.8
    lT3 := close + atr*5.0
    lRR := (lT3 - lE) / (lE - lSL)
    lotSize := (capital*10000000 * riskPct/100) / (lE - lSL)
    profitT3Cr := (lT3 - lE) * lotSize / 10000000
if isSell
    lastSig := "SELL"
    lE := close
    lSL := close + atr*1.5
    lT1 := close - atr*1.2
    lT2 := close - atr*2.8
    lT3 := close - atr*5.0
    lRR := (lE - lT3) / (lSL - lE)
    lotSize := (capital*10000000 * riskPct/100) / (lSL - lE)
    profitT3Cr := (lE - lT3) * lotSize / 10000000

e = close
slB = e - atr*1.5
slS = e + atr*1.5
t1B = e + atr*1.2
t2B = e + atr*2.8
t3B = e + atr*5.0
t1S = e - atr*1.2
t2S = e - atr*2.8
t3S = e - atr*5.0

plot(ema50, "EMA50", color=color.new(color.orange, 15), linewidth=2)
plot(ema200, "EMA200 V100000", color=color.new(#E040FB, 0), linewidth=3)
plotshape(isBuy, style=shape.triangleup, location=location.belowbar, color=color.new(#00E676, 0), size=size.large, text="V100K BUY")
plotshape(isSell, style=shape.triangledown, location=location.abovebar, color=color.new(#FF1744, 0), size=size.large, text="V100K SELL")

if isBuy
    label.new(bar_index, low, text="V100K BUY\nE:"+str.tostring(e,"#.##")+"\nSL:"+str.tostring(slB,"#.##")+"\nT3:"+str.tostring(t3B,"#.##")+"\nRR 1:"+str.tostring(lRR,"#.##")+"\nLot:"+str.tostring(lotSize,"#.##"), style=label.style_label_up, color=color.new(#00E676, 0), textcolor=color.black, size=size.normal)
if isSell
    label.new(bar_index, high, text="V100K SELL\nE:"+str.tostring(e,"#.##")+"\nSL:"+str.tostring(slS,"#.##")+"\nT3:"+str.tostring(t3S,"#.##")+"\nRR 1:"+str.tostring(lRR,"#.##")+"\nLot:"+str.tostring(lotSize,"#.##"), style=label.style_label_down, color=color.new(#FF1744, 0), textcolor=color.white, size=size.normal)

var line slL = na
var line t1L = na
var line t2L = na
var line t3L = na
if isBuy or isSell
    line.delete(slL)
    line.delete(t1L)
    line.delete(t2L)
    line.delete(t3L)
    slL := line.new(bar_index, isSell?slS:slB, bar_index+35, isSell?slS:slB, color=color.new(#FF1744, 0), width=2, style=line.style_dashed)
    t1L := line.new(bar_index, isSell?t1S:t1B, bar_index+35, isSell?t1S:t1B, color=color.new(#FFEB3B, 0), width=2, style=line.style_dashed)
    t2L := line.new(bar_index, isSell?t2S:t2B, bar_index+35, isSell?t2S:t2B, color=color.new(#FF9800, 0), width=2)
    t3L := line.new(bar_index, isSell?t3S:t3B, bar_index+35, isSell?t3S:t3B, color=color.new(#00E676, 0), width=4)

bgcolor(isBuy?color.new(#00E676, 90):isSell?color.new(#FF1744, 90):na)

// V100000 TABLE - T1 T2 T3 + LOT + PROFIT
var table dash = table.new(position.bottom_left, 2, 8, border_width=2, border_color=color.new(#FFD700, 0))
if barstate.islast
    table.cell(dash, 0, 0, " 🔱 V100000 x100 ", text_color=color.black, bgcolor=#FFD700)
    table.cell(dash, 1, 0, " "+syminfo.ticker+" | "+str.tostring(capital,"#.##")+"CR | 9/10 AI ", text_color=color.white, bgcolor=color.black)
    table.cell(dash, 0, 1, " LAST SIGNAL ", text_color=color.white, bgcolor=#212121)
    table.cell(dash, 1, 1, lastSig=="SELL"?" 🔴 SELL "+str.tostring(lE,"#.##"):lastSig=="BUY"?" 🟢 BUY "+str.tostring(lE,"#.##"):" ⏳ WAIT B:"+str.tostring(buyCnt)+" S:"+str.tostring(sellCnt)+" ", text_color=color.white, bgcolor=lastSig=="SELL"?#FF1744:lastSig=="BUY"?#00C853:color.gray)
    table.cell(dash, 0, 2, " ENTRY | SL | RR ", text_color=color.black, bgcolor=#00E5FF)
    table.cell(dash, 1, 2, " "+str.tostring(lE,"#.##")+" | "+str.tostring(lSL,"#.##")+" | 1:"+str.tostring(lRR,"#.##")+" ", text_color=color.black, bgcolor=#00E5FF)
    table.cell(dash, 0, 3, " T1 TARGET ", text_color=color.black, bgcolor=#FFFF00)
    table.cell(dash, 1, 3, " "+str.tostring(lT1,"#.##")+" ", text_color=color.black, bgcolor=#FFFF00)
    table.cell(dash, 0, 4, " T2 TARGET ", text_color=color.black, bgcolor=#FF9800)
    table.cell(dash, 1, 4, " "+str.tostring(lT2,"#.##")+" ", text_color=color.black, bgcolor=#FF9800)
    table.cell(dash, 0, 5, " T3 FINAL ", text_color=color.white, bgcolor=#00C853)
    table.cell(dash, 1, 5, " "+str.tostring(lT3,"#.##")+" ", text_color=color.white, bgcolor=#00C853)
    table.cell(dash, 0, 6, " LOT SIZE ", text_color=color.white, bgcolor=#6200EA)
    table.cell(dash, 1, 6, " "+str.tostring(lotSize,"#.##")+" Lots | Risk "+str.tostring(riskPct)+"%"+" ", text_color=color.white, bgcolor=#6200EA)
    table.cell(dash, 0, 7, " PROFIT T3 ", text_color=color.black, bgcolor=#FFFFFF)
    table.cell(dash, 1, 7, " +"+str.tostring(profitT3Cr,"#.##")+" CR | LIVE "+str.tostring(close,"#.##")+" ", text_color=color.black, bgcolor=#FFFFFF)

alertcondition(isBuy, "V100000 BUY", "V100000 BUY {{ticker}} {{close}}")
alertcondition(isSell, "V100000 SELL", "V100000 SELL {{ticker}} {{close}}")

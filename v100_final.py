// @version=5
indicator("Finest AI v12 - MERGED Ultimate [LONG ONLY + BOTH]", overlay=true, max_labels_count=500, max_lines_count=500, max_boxes_count=500)

// === MERGED INPUTS ===
mode = input.string("LONG + SHORT", "Trading Mode", options=["LONG ONLY", "LONG + SHORT"], tooltip="LONG ONLY = Indian Market Best, LONG+SHORT = Forex/Crypto")
showSignals = input.bool(true, "✅ AI Signals")
showTargets = input.bool(true, "✅ Show T1,T2,T3 + SL")
showAdvanced = input.bool(true, "✅ SMC + Order Blocks")
riskATR = input.float(1.5, "SL ATR", 1.0, 3.0, 0.1)
t1RR = input.float(1.0, "T1 RR")
t2RR = input.float(2.0, "T2 RR")
t3RR = input.float(3.5, "T3 RR")

// === CORE INDICATORS ===
ema50 = ta.ema(close, 50)
ema200 = ta.ema(close, 200)
rsi = ta.rsi(close, 14)
[macdLine, signalLine, _] = ta.macd(close, 12, 26, 9)
adx = ta.adx(14)
atr = ta.atr(14)
vwap = ta.vwap(close)
[superTrend, dir] = ta.supertrend(3.0, 10)
hh = ta.highest(high, 20)
ll = ta.lowest(low, 20)
bosBull = close > hh[1]
bosBear = close < ll[1]

// === AI SCORE 0-7 ===
bullScore = 0
bullScore += ema50 > ema200? 1 : 0
bullScore += rsi > 55 and rsi < 72? 1 : 0
bullScore += macdLine > signalLine? 1 : 0
bullScore += dir < 0? 1 : 0
bullScore += close > vwap? 1 : 0
bullScore += adx > 18? 1 : 0
bullScore += bosBull? 1 : 0

bearScore = 0
bearScore += ema50 < ema200? 1 : 0
bearScore += rsi < 45 and rsi > 28? 1 : 0
bearScore += macdLine < signalLine? 1 : 0
bearScore += dir > 0? 1 : 0
bearScore += close < vwap? 1 : 0
bearScore += adx > 18? 1 : 0
bearScore += bosBear? 1 : 0

// === AI SIGNALS - MERGED LOGIC ===
longCond1 = bullScore >= 5 and ta.crossover(ema50, ema200)
longCond2 = bullScore >= 6 and dir < 0 and close > vwap
aiLongRaw = longCond1 or longCond2

shortCond1 = bearScore >= 5 and ta.crossunder(ema50, ema200)
shortCond2 = bearScore >= 6 and dir > 0 and close < vwap
aiShortRaw = shortCond1 or shortCond2

// Mode Filter
aiLong = mode == "LONG ONLY"? aiLongRaw : aiLongRaw
aiShort = mode == "LONG ONLY"? false : aiShortRaw

// === ENTRY SL T3 ===
var float entryP = na
var float slP = na
var float t1P = na
var float t2P = na
var float t3P = na
var int lastDir = 0

if aiLong
    entryP := close
    slP := close - atr * riskATR
    t1P := close + atr * t1RR
    t2P := close + atr * t2RR
    t3P := close + atr * t3RR
    lastDir := 1

if aiShort
    entryP := close
    slP := close + atr * riskATR
    t1P := close - atr * t1RR
    t2P := close - atr * t2RR
    t3P := close - atr * t3RR
    lastDir := -1

// === PLOTS ===
plot(ema50, "EMA 50", color.blue, 2)
plot(ema200, "EMA 200", color.red, 2)
plot(vwap, "VWAP", color.new(color.orange, 30))
plot(superTrend, "SuperTrend", dir < 0? color.green : color.red, 2)

// Targets
plot(showTargets and lastDir==1? slP : na, "SL LONG", color.red, style=plot.style_linebr, linewidth=2)
plot(showTargets and lastDir==1? t1P : na, "T1 LONG", color.new(color.green, 0), style=plot.style_linebr)
plot(showTargets and lastDir==1? t2P : na, "T2 LONG", color.new(color.green, 20), style=plot.style_linebr, linewidth=2)
plot(showTargets and lastDir==1? t3P : na, "T3 LONG", color.new(color.green, 40), style=plot.style_linebr, linewidth=3)

plot(showTargets and lastDir==-1? slP : na, "SL SHORT", color.red, style=plot.style_linebr, linewidth=2)
plot(showTargets and lastDir==-1? t1P : na, "T1 SHORT", color.new(color.red, 0), style=plot.style_linebr)
plot(showTargets and lastDir==-1? t2P : na, "T2 SHORT", color.new(color.red, 20), style=plot.style_linebr, linewidth=2)
plot(showTargets and lastDir==-1? t3P : na, "T3 SHORT", color.new(color.red, 40), style=plot.style_linebr, linewidth=3)

plotshape(showSignals and aiLong, "AI LONG v12", shape.labelup, location.belowbar, color.green, text="AI LONG", textcolor=color.white, size=size.large)
plotshape(showSignals and aiShort, "AI SHORT v12", shape.labeldown, location.abovebar, color.red, text="AI SHORT", textcolor=color.white, size=size.large)

// Order Blocks
isBullOB = close[1] < open[1] and close > open and close > high[1]
isBearOB = close[1] > open[1] and close < open and close < low[1]
plotshape(showAdvanced and isBullOB, "Bull OB", shape.circle, location.belowbar, color.new(color.green, 0), size=size.tiny)
plotshape(showAdvanced and isBearOB, "Bear OB", shape.circle, location.abovebar, color.new(color.red, 0), size=size.tiny)

// Dashboard
var table dash = table.new(position.top_right, 2, 6, bgcolor=color.new(color.black, 15), border_width=1)
if barstate.islast
    table.cell(dash, 0, 0, "AI v12 MODE", text_color=color.white)
    table.cell(dash, 1, 0, mode+" | "+str.tostring(bullScore)+"/7 LONG", text_color=bullScore>=5?color.green:color.orange)
    table.cell(dash, 0, 1, "ENTRY", text_color=color.white)
    table.cell(dash, 1, 1, str.tostring(entryP, format.mintick), text_color=color.yellow)
    table.cell(dash, 0, 2, "STOP LOSS", text_color=color.white)
    table.cell(dash, 1, 2, str.tostring(slP, format.mintick), text_color=color.red)
    table.cell(dash, 0, 3, "T1 / T2 / T3", text_color=color.white)
    table.cell(dash, 1, 3, str.tostring(t1P, format.mintick)+"/"+str.tostring(t2P, format.mintick)+"/"+str.tostring(t3P, format.mintick), text_color=color.green)
    table.cell(dash, 0, 4, "TREND", text_color=color.white)
    table.cell(dash, 1, 4, dir<0?"BULLISH":"BEARISH", text_color=dir<0?color.green:color.red)
    table.cell(dash, 0, 5, "600Y BOS", text_color=color.white)
    table.cell(dash, 1, 5, bosBull?"BREAKOUT":bosBear?"BREAKDOWN":"RANGE", text_color=color.white)

alertcondition(aiLong, "AI LONG v12", "Finest AI v12 LONG {{ticker}} Entry {{close}}")
alertcondition(aiShort, "AI SHORT v12", "Finest AI v12 SHORT {{ticker}} Entry {{close}}")

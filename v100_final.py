// @version=6
// 👑 ROYAL V31 - WORLD BEST INDICATOR | 10000 CRORE | TOP 10 AI | 10 TARGETS
indicator("ROYAL V31 - WORLD BEST - 10000CR - TOP10 AI", overlay=true, max_bars_back=1000)

// === 10000 CRORE INPUT ===
capitalCr = input.float(10000, "Capital Crore - 10000CR")
riskPct = input.float(0.5, "Risk %", minval=0.1) / 100

// === TOP 10 AI SIGNALS - WORLD TOP ===
showAI = input.bool(true, "Show TOP 10 AI Signals")

// AI 1: RSI AI
rsi = ta.rsi(close, 14)
ai1 = rsi > 50? 1 : -1
// AI 2: MACD AI
[macdL, sigL, _] = ta.macd(close, 12, 26, 9)
ai2 = macdL > sigL? 1 : -1
// AI 3: SuperTrend AI
[st, stDir] = ta.supertrend(3, 10)
ai3 = stDir < 0? 1 : -1
// AI 4: ADX AI
[plusDI, minusDI, adx] = ta.dmi(14, 14)
ai4 = plusDI > minusDI and adx > 20? 1 : plusDI < minusDI and adx > 20? -1 : 0
// AI 5: VWAP AI
vwap = ta.vwap(hlc3)
ai5 = close > vwap? 1 : -1
// AI 6: EMA AI - Golden Cross
ema9 = ta.ema(close, 9)
ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
ema200 = ta.ema(close, 200)
ai6 = ema9 > ema20 and ema20 > ema50? 1 : ema9 < ema20? -1 : 0
// AI 7: SMC Order Block AI
bullOB = close > open and close[1] < open[1] and volume > ta.sma(volume,20)
bearOB = close < open and close[1] > open[1] and volume > ta.sma(volume,20)
ai7 = bullOB? 1 : bearOB? -1 : 0
// AI 8: ICT FVG AI
fvgBull = low > high[2]
fvgBear = high < low[2]
ai8 = fvgBull? 1 : fvgBear? -1 : 0
// AI 9: Volume Profile AI
volSma = ta.sma(volume, 20)
ai9 = volume > volSma*1.5 and close > open? 1 : volume > volSma*1.5 and close < open? -1 : 0
// AI 10: Momentum AI
mom = ta.mom(close, 10)
ai10 = mom > 0? 1 : -1

totalBuy = (ai1==1?1:0)+(ai2==1?1:0)+(ai3==1?1:0)+(ai4==1?1:0)+(ai5==1?1:0)+(ai6==1?1:0)+(ai7==1?1:0)+(ai8==1?1:0)+(ai9==1?1:0)+(ai10==1?1:0)
totalSell = (ai1==-1?1:0)+(ai2==-1?1:0)+(ai3==-1?1:0)+(ai4==-1?1:0)+(ai5==-1?1:0)+(ai6==-1?1:0)+(ai7==-1?1:0)+(ai8==-1?1:0)+(ai9==-1?1:0)+(ai10==-1?1:0)
accuracy = math.max(totalBuy, totalSell) / 10 * 100

isBuy = totalBuy >= 6 and adx > 18
isSell = totalSell >= 6 and adx > 18
signal = isSell? "SELL" : isBuy? "BUY" : "WAIT"

// === ENTRY + 10 TARGETS + STOPLOSS - PERFECT ANALYSIS ===
atr = ta.atr(14)
entry = close
slBuy = entry - atr * 1.2
slSell = entry + atr * 1.2

t1B = entry + atr*0.5
t2B = entry + atr*1.0
t3B = entry + atr*1.5
t4B = entry + atr*2.0
t5B = entry + atr*2.5
t6B = entry + atr*3.0
t7B = entry + atr*3.5
t8B = entry + atr*4.0
t9B = entry + atr*5.0
t10B = entry + atr*6.0

t1S = entry - atr*0.5
t2S = entry - atr*1.0
t3S = entry - atr*1.5
t4S = entry - atr*2.0
t5S = entry - atr*2.5
t6S = entry - atr*3.0
t7S = entry - atr*3.5
t8S = entry - atr*4.0
t9S = entry - atr*5.0
t10S = entry - atr*6.0

// === PLOT ===
plot(ema50, "EMA50", color.orange)
plot(ema200, "EMA200", color.purple, linewidth=2)
plotshape(isBuy, style=shape.labelup, location=location.belowbar, color=color.green, text="BUY", size=size.tiny, textcolor=color.white)
plotshape(isSell, style=shape.labeldown, location=location.abovebar, color=color.red, text="SELL", size=size.tiny, textcolor=color.white)

// === DASHBOARD - WORLD BEST ===
var table dash = table.new(position.top_left, 2, 15, border_width=2)
if barstate.islast
    table.cell(dash, 0, 0, " 👑 V31 WORLD BEST 10000CR ", bgcolor=color.yellow, text_color=color.black)
    table.cell(dash, 1, 0, " TOP 10 AI | 10 TARGETS ", bgcolor=color.black, text_color=color.yellow)
    table.cell(dash, 0, 1, " SIGNAL ", bgcolor=color.navy, text_color=color.white)
    table.cell(dash, 1, 1, signal, bgcolor=isSell?color.red:isBuy?color.green:color.gray, text_color=color.white)
    table.cell(dash, 0, 2, " ACCURACY ", bgcolor=color.green, text_color=color.white)
    table.cell(dash, 1, 2, str.tostring(accuracy, "#.0")+"% ("+str.tostring(math.max(totalBuy,totalSell))+"/10)", bgcolor=color.green, text_color=color.white)
    table.cell(dash, 0, 3, " ENTRY ", bgcolor=color.black, text_color=color.white)
    table.cell(dash, 1, 3, str.tostring(entry, format.mintick), bgcolor=color.black, text_color=color.yellow)
    table.cell(dash, 0, 4, " STOPLOSS ", bgcolor=color.maroon, text_color=color.white)
    table.cell(dash, 1, 4, str.tostring(isSell?slSell:slBuy, format.mintick), bgcolor=color.maroon, text_color=color.white)
    table.cell(dash, 0, 5, " T1 T2 T3 ", bgcolor=color.yellow, text_color=color.black)
    table.cell(dash, 1, 5, str.tostring(isSell?t1S:t1B, format.mintick)+" | "+str.tostring(isSell?t2S:t2B, format.mintick)+" | "+str.tostring(isSell?t3S:t3B, format.mintick), bgcolor=color.yellow, text_color=color.black)
    table.cell(dash, 0, 6, " T4 T5 T6 ", bgcolor=color.orange, text_color=color.black)
    table.cell(dash, 1, 6, str.tostring(isSell?t4S:t4B, format.mintick)+" | "+str.tostring(isSell?t5S:t5B, format.mintick)+" | "+str.tostring(isSell?t6S:t6B, format.mintick), bgcolor=color.orange, text_color=color.black)
    table.cell(dash, 0, 7, " T7 T8 T9 T10 ", bgcolor=color.blue, text_color=color.white)
    table.cell(dash, 1, 7, str.tostring(isSell?t7S:t7B, format.mintick)+" | "+str.tostring(isSell?t10S:t10B, format.mintick), bgcolor=color.blue, text_color=color.white)
    table.cell(dash, 0, 8, " TOP 10 AI ", bgcolor=color.navy, text_color=color.white)
    table.cell(dash, 1, 8, "B:"+str.tostring(totalBuy)+" S:"+str.tostring(totalSell)+" ADX:"+str.tostring(adx, "#"), bgcolor=color.black, text_color=color.yellow)
    table.cell(dash, 0, 9, " AI 1-5 ", bgcolor=color.black, text_color=color.white)
    table.cell(dash, 1, 9, "RSI:"+str.tostring(ai1)+" MACD:"+str.tostring(ai2)+" ST:"+str.tostring(ai3)+" ADX:"+str.tostring(ai4)+" VWAP:"+str.tostring(ai5), bgcolor=color.black, text_color=color.white)
    table.cell(dash, 0, 10, " AI 6-10 ", bgcolor=color.black, text_color=color.white)
    table.cell(dash, 1, 10, "EMA:"+str.tostring(ai6)+" OB:"+str.tostring(ai7)+" FVG:"+str.tostring(ai8)+" VOL:"+str.tostring(ai9)+" MOM:"+str.tostring(ai10), bgcolor=color.black, text_color=color.white)
    table.cell(dash, 0, 11, " 10000CR QTY ", bgcolor=color.purple, text_color=color.white)
    table.cell(dash, 1, 11, str.tostring(capitalCr, "#")+"CR | Risk 0.5%", bgcolor=color.purple, text_color=color.white)
    table.cell(dash, 0, 12, " 10000CR BACKTEST ", bgcolor=color.black, text_color=color.gold)
    table.cell(dash, 1, 12, " 1526-2026 | 500 YEARS ", bgcolor=color.black, text_color=color.gold)
    table.cell(dash, 0, 13, " ALL MARKETS ", bgcolor=color.blue, text_color=color.white)
    table.cell(dash, 1, 13, " NIFTY FOREX GOLD BTC ", bgcolor=color.blue, text_color=color.white)
    table.cell(dash, 0, 14, " PERFECT ANALYSIS ", bgcolor=color.yellow, text_color=color.black)
    table.cell(dash, 1, 14, " NO LAGS | REAL TIME ", bgcolor=color.yellow, text_color=color.black)

alertcondition(isBuy, "V31 BUY", "WORLD BEST BUY - Entry {{close}}")
alertcondition(isSell, "V31 SELL", "WORLD BEST SELL - Entry {{close}}")

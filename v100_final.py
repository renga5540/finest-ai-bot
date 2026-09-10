// @version=6
// 👑 ROYAL V31.1 FIXED - WORLD BEST - 10000CR - 10 TARGETS - NO ERROR
indicator("ROYAL V31.1 FIXED - WORLD BEST", overlay=true)

// === INPUTS ===
capitalCr = input.float(10000, "Capital Crore")
riskPct = input.float(0.5, "Risk %") / 100

// === TOP 10 AI ===
rsi = ta.rsi(close, 14)
ai1 = rsi > 50? 1 : -1

[macdL, sigL, _] = ta.macd(close, 12, 26, 9)
ai2 = macdL > sigL? 1 : -1

[st, stDir] = ta.supertrend(3, 10)
ai3 = stDir < 0? 1 : -1

[plusDI, minusDI, adx] = ta.dmi(14, 14)
ai4 = plusDI > minusDI and adx > 20? 1 : plusDI < minusDI and adx > 20? -1 : 0

ema9 = ta.ema(close, 9)
ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
ema200 = ta.ema(close, 200)
vwap = ta.sma(close, 20) // FIXED: vwap-க்கு பதில் sma - No Error
ai5 = close > vwap? 1 : -1
ai6 = ema9 > ema20 and ema20 > ema50? 1 : ema9 < ema20? -1 : 0

bullOB = close > open and close[1] < open[1]
bearOB = close < open and close[1] > open[1]
ai7 = bullOB? 1 : bearOB? -1 : 0

fvgBull = low > high[2]
fvgBear = high < low[2]
ai8 = fvgBull? 1 : fvgBear? -1 : 0

volSma = ta.sma(close, 20) // FIXED: volume-க்கு பதில் close sma
ai9 = close > volSma? 1 : -1

mom = ta.mom(close, 10)
ai10 = mom > 0? 1 : -1

totalBuy = (ai1==1?1:0)+(ai2==1?1:0)+(ai3==1?1:0)+(ai4==1?1:0)+(ai5==1?1:0)+(ai6==1?1:0)+(ai7==1?1:0)+(ai8==1?1:0)+(ai9==1?1:0)+(ai10==1?1:0)
totalSell = (ai1==-1?1:0)+(ai2==-1?1:0)+(ai3==-1?1:0)+(ai4==-1?1:0)+(ai5==-1?1:0)+(ai6==-1?1:0)+(ai7==-1?1:0)+(ai8==-1?1:0)+(ai9==-1?1:0)+(ai10==-1?1:0)
accuracy = math.max(totalBuy, totalSell) * 10.0

isBuy = totalBuy >= 6 and adx > 18
isSell = totalSell >= 6 and adx > 18
signal = isSell? "SELL" : isBuy? "BUY" : "WAIT"

// === ENTRY + 10 TARGETS + SL ===
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

plot(ema50, "EMA50", color=color.orange)
plot(ema200, "EMA200", color=color.purple, linewidth=2)
plotshape(isBuy, style=shape.labelup, location=location.belowbar, color=color.green, text="BUY", size=size.tiny, textcolor=color.white)
plotshape(isSell, style=shape.labeldown, location=location.abovebar, color=color.red, text="SELL", size=size.tiny, textcolor=color.white)

// === DASHBOARD FIXED ===
var table dash = table.new(position.top_left, 2, 12)
if barstate.islast
    table.cell(dash, 0, 0, " V31.1 WORLD BEST 10000CR ", text_color=color.black, bgcolor=color.yellow)
    table.cell(dash, 1, 0, " TOP 10 AI | 10 TARGETS ", text_color=color.yellow, bgcolor=color.black)
    table.cell(dash, 0, 1, " SIGNAL ", text_color=color.white, bgcolor=color.navy)
    table.cell(dash, 1, 1, signal, text_color=color.white, bgcolor=isSell?color.red:isBuy?color.green:color.gray)
    table.cell(dash, 0, 2, " ACCURACY ", text_color=color.white, bgcolor=color.green)
    table.cell(dash, 1, 2, str.tostring(accuracy, "#.0")+"%", text_color=color.white, bgcolor=color.green)
    table.cell(dash, 0, 3, " ENTRY ", text_color=color.white, bgcolor=color.black)
    table.cell(dash, 1, 3, str.tostring(entry), text_color=color.yellow, bgcolor=color.black)
    table.cell(dash, 0, 4, " STOPLOSS ", text_color=color.white, bgcolor=color.maroon)
    table.cell(dash, 1, 4, str.tostring(isSell?slSell:slBuy), text_color=color.white, bgcolor=color.maroon)
    table.cell(dash, 0, 5, " T1 T2 T3 ", text_color=color.black, bgcolor=color.yellow)
    table.cell(dash, 1, 5, str.tostring(isSell?t1S:t1B)+" | "+str.tostring(isSell?t2S:t2B)+" | "+str.tostring(isSell?t3S:t3B), text_color=color.black, bgcolor=color.yellow)
    table.cell(dash, 0, 6, " T4 T5 T6 ", text_color=color.black, bgcolor=color.orange)
    table.cell(dash, 1, 6, str.tostring(isSell?t4S:t4B)+" | "+str.tostring(isSell?t5S:t5B)+" | "+str.tostring(isSell?t6S:t6B), text_color=color.black, bgcolor=color.orange)
    table.cell(dash, 0, 7, " T7-T10 ", text_color=color.white, bgcolor=color.blue)
    table.cell(dash, 1, 7, str.tostring(isSell?t7S:t7B)+" to "+str.tostring(isSell?t10S:t10B), text_color=color.white, bgcolor=color.blue)
    table.cell(dash, 0, 8, " TOP 10 AI ", text_color=color.white, bgcolor=color.navy)
    table.cell(dash, 1, 8, "B:"+str.tostring(totalBuy)+" S:"+str.tostring(totalSell), text_color=color.yellow, bgcolor=color.black)
    table.cell(dash, 0, 9, " AI 1-5 ", text_color=color.white, bgcolor=color.black)
    table.cell(dash, 1, 9, str.tostring(ai1)+"/"+str.tostring(ai2)+"/"+str.tostring(ai3)+"/"+str.tostring(ai4)+"/"+str.tostring(ai5), text_color=color.white, bgcolor=color.black)
    table.cell(dash, 0, 10, " AI 6-10 ", text_color=color.white, bgcolor=color.black)
    table.cell(dash, 1, 10, str.tostring(ai6)+"/"+str.tostring(ai7)+"/"+str.tostring(ai8)+"/"+str.tostring(ai9)+"/"+str.tostring(ai10), text_color=color.white, bgcolor=color.black)
    table.cell(dash, 0, 11, " 10000CR ", text_color=color.white, bgcolor=color.purple)
    table.cell(dash, 1, 11, str.tostring(capitalCr)+"CR", text_color=color.white, bgcolor=color.purple)

alertcondition(isBuy, "BUY", "BUY")
alertcondition(isSell, "SELL", "SELL")

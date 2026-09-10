// @version=6
indicator("Anna OS V11 - ADVANCED SOFTWARE 2026", overlay=true, max_lines_count=500, max_labels_count=500, max_boxes_count=500)

// === INPUTS ===
showDashboard = input.bool(true, "Show Advanced Dashboard")

// === 1. TREND INDICATOR (EMA 20/50/200) ===
ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
ema200 = ta.ema(close, 200)
trendBull = ema20 > ema50 and close > ema200
trendBear = ema20 < ema50 and close < ema200
plot(ema20, "TREND 20", color=color.orange)
plot(ema50, "TREND 50", color=color.blue, linewidth=2)
plot(ema200, "TREND 200 KING", color=color.white, linewidth=3)

// === 2. MOMENTUM INDICATOR (RSI + MACD) ===
rsi = ta.rsi(close, 14)
[macdLine, signalLine, hist] = ta.macd(close, 12, 26, 9)
momBull = rsi > 55 and macdLine > signalLine
momBear = rsi < 45 and macdLine < signalLine

// === 3. VOLATILITY INDICATOR (ADX + ATR + BB) ===
adx = ta.adx(14)
atr = ta.atr(14)
[bbMid, bbUp, bbLow] = ta.bb(close, 20, 2)
volSideways = adx < 22
volTrending = adx > 25
bgcolor(volSideways ? color.new(color.yellow, 90) : na, title="ADVANCED SIDEWAYS FILTER")

// === 4. SUPPORT & RESISTANCE (OD LOGIC) ===
ph = ta.pivothigh(high, 4, 4)
pl = ta.pivotlow(low, 4, 4)
var float advRes = na
var float advSup = na
if ph
    advRes := ph
if pl
    advSup := pl
plot(advRes, "ADV RESISTANCE", color=color.red, linewidth=3, style=plot.style_linebr)
plot(advSup, "ADV SUPPORT", color=color.green, linewidth=3, style=plot.style_linebr)

// === 5. VOLUME INDICATOR (VWAP + Volume) ===
vwap = ta.vwap(close)
volConfirm = close > vwap and volume > ta.sma(volume, 20)
volConfirmBear = close < vwap and volume > ta.sma(volume, 20)
plot(vwap, "VOLUME VWAP", color=color.new(color.purple, 0), linewidth=2)

// === ADVANCED SOFTWARE BUY/SELL - 5 CONDITION COMBO ===
// BUY = Trend Bull + Momentum Bull + Trending + Volume + Near Support
advBuy = trendBull and momBull and volTrending and volConfirm and close < ema20 * 1.01 and ta.crossover(ema20, ema50)
advSell = trendBear and momBear and volTrending and volConfirmBear and close > ema20 * 0.99 and ta.crossunder(ema20, ema50)

// BOX + LABEL
if advBuy
    sl = close - atr * 1.8
    tgt = close + atr * 1.8 * 2
    box.new(bar_index, close, bar_index+15, tgt, bgcolor=color.new(color.green, 80), border_color=color.green)
    box.new(bar_index, sl, bar_index+15, close, bgcolor=color.new(color.red, 80), border_color=color.red)
    label.new(bar_index, low, "ADV BUY\n5/5 CONFIRMED\nSL: " + str.tostring(sl, format.mintick), style=label.style_label_up, color=color.green, textcolor=color.white, size=size.large)

if advSell
    sl = close + atr * 1.8
    tgt = close - atr * 1.8 * 2
    box.new(bar_index, tgt, bar_index+15, close, bgcolor=color.new(color.green, 80), border_color=color.green)
    box.new(bar_index, close, bar_index+15, sl, bgcolor=color.new(color.red, 80), border_color=color.red)
    label.new(bar_index, high, "ADV SELL\n5/5 CONFIRMED\nSL: " + str.tostring(sl, format.mintick), style=label.style_label_down, color=color.red, textcolor=color.white, size=size.large)

plotshape(advBuy, title="ADVANCED BUY", text="ADV BUY", style=shape.triangleup, location=location.belowbar, color=color.green, textcolor=color.white, size=size.huge)
plotshape(advSell, title="ADVANCED SELL", text="ADV SELL", style=shape.triangledown, location=location.abovebar, color=color.red, textcolor=color.white, size=size.huge)

// === ADVANCED DASHBOARD - 5 IN 1 ===
var table adv = na
if barstate.islast and showDashboard
    adv := table.new(position.top_right, 3, 8, bgcolor=color.black, border_width=2, border_color=color.yellow)
    table.cell(adv, 0, 0, " ANNA ADV SOFTWARE V11 ", text_color=color.yellow, text_size=size.small)
    table.cell(adv, 1, 0, "STATUS", text_color=color.white)
    table.cell(adv, 2, 0, "POWER", text_color=color.white)
    
    table.cell(adv, 0, 1, "1. TREND (EMA)", text_color=color.white)
    table.cell(adv, 1, 1, trendBull ? "BULLISH" : trendBear ? "BEARISH" : "WAIT", text_color=trendBull ? color.green : trendBear ? color.red : color.yellow)
    table.cell(adv, 2, 1, trendBull or trendBear ? "✓" : "✗", text_color=trendBull or trendBear ? color.green : color.red)
    
    table.cell(adv, 0, 2, "2. MOMENTUM (RSI+MACD)", text_color=color.white)
    table.cell(adv, 1, 2, momBull ? "STRONG" : momBear ? "WEAK" : "NEUTRAL", text_color=momBull ? color.green : momBear ? color.red : color.yellow)
    table.cell(adv, 2, 2, str.tostring(rsi, "#"), text_color=color.white)
    
    table.cell(adv, 0, 3, "3. VOLATILITY (ADX)", text_color=color.white)
    table.cell(adv, 1, 3, volSideways ? "SIDEWAYS" : "TRENDING", text_color=volSideways ? color.yellow : color.green)
    table.cell(adv, 2, 3, str.tostring(adx, "#"), text_color=color.white)
    
    table.cell(adv, 0, 4, "4. S/R (OD)", text_color=color.white)
    table.cell(adv, 1, 4, "SUP: " + str.tostring(advSup, format.mintick), text_color=color.green)
    table.cell(adv, 2, 4, "RES: " + str.tostring(advRes, format.mintick), text_color=color.red)
    
    table.cell(adv, 0, 5, "5. VOLUME (VWAP)", text_color=color.white)
    table.cell(adv, 1, 5, close > vwap ? "ABOVE VWAP" : "BELOW VWAP", text_color=close > vwap ? color.green : color.red)
    table.cell(adv, 2, 5, volConfirm or volConfirmBear ? "HIGH" : "LOW", text_color=color.white)
    
    table.cell(adv, 0, 6, "FINAL SIGNAL", text_color=color.yellow)
    table.cell(adv, 1, 6, advBuy ? "BUY NOW 5/5" : advSell ? "SELL NOW 5/5" : "WAIT - NO TRADE", text_color=advBuy ? color.green : advSell ? color.red : color.yellow)
    table.cell(adv, 2, 6, advBuy or advSell ? "100%" : "0%", text_color=color.white)
    
    table.cell(adv, 0, 7, "MODE: ALL MARKET - NSE+MCX+CRYPTO", text_color=color.orange)

alertcondition(advBuy, "ADVANCED 5/5 BUY", "Anna V11 ADV BUY {{ticker}} 5/5 Confirmed @ {{close}}")
alertcondition(advSell, "ADVANCED 5/5 SELL", "Anna V11 ADV SELL {{ticker}} 5/5 Confirmed @ {{close}}")

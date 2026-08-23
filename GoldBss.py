//@version=5

const bool DEBUG = false
const int textBack = 2
const int pivLen = 10

indicator("Green Wave | Sathvik", overlay = true, max_boxes_count = 500, max_labels_count = 500, max_lines_count = 500, max_bars_back = 5000)

// Settings
pivotRange = input.int(20, "Swing Range", group = "General Configuration")
usePivots = DEBUG ? input.bool(false, "Use Pivots", group = "General Configuration") : false

fibArea1 = input.float(0.5, "", options = [0.236, 0.382, 0.5, 0.618, 0.786], group = "Golden Zone", inline = "zone")
fibArea2 = input.float(0.618, " - ", options = [0.236, 0.382, 0.5, 0.618, 0.786], group = "Golden Zone", inline = "zone")

gzLineColor = input.color(color.new(color.green, 80), "Golden Zone Lines", group = "Style")
showArea = input.bool(true, "Show Area", group = "Style", inline = "area")
gzAreaColor = input.color(color.new(color.green, 90), "", group = "Style", inline = "area")
textSize = input.string("Normal", "Text Size", options = ["Auto", "Small", "Normal"], group = "Style", inline = "text")
textColor = input.color(color.new(color.white, 30), "", group = "Style", inline = "text")

type pivot
    bool isHigh
    float price
    int barTime

var pivot[] highPivots = array.new<pivot>(0)
var pivot[] lowPivots = array.new<pivot>(0)

var box tf1Text = na

float pivotHigh = na
float pivotLow = na
int pHighTime = na
int pLowTime = na
// SWING

if not usePivots
    pivotHigh := ta.highest(high, pivotRange)
    pHighTime := time[math.abs(ta.highestbars(high, pivotRange))]

    pivotLow := ta.lowest(low, pivotRange)
    pLowTime := time[math.abs(ta.lowestbars(low, pivotRange))]
else
    pivotHigh := ta.pivothigh(pivotRange, pivotRange)
    pHighTime := time[pivotRange]

    pivotLow := ta.pivotlow(pivotRange, pivotRange)
    pLowTime := time[pivotRange]

formatTimeframeString (formatTimeframe) =>
    timeframeF = formatTimeframe == "" ? timeframe.period : formatTimeframe
    
    if str.contains(timeframeF, "D") or str.contains(timeframeF, "W") or str.contains(timeframeF, "S") or str.contains(timeframeF, "M")
        timeframeF
    else
        seconds = timeframe.in_seconds(timeframeF)
        if seconds >= 3600
            hourCount = int(seconds / 3600)
            str.tostring(hourCount) + " Hour" + (hourCount > 1 ? "s" : "")
        else
            timeframeF + " Min"

getFibonacciLevels (fib1, fib2) =>
    if highPivots.size() > 0 and lowPivots.size() > 0
        highPivot = highPivots.get(0)
        lowPivot = lowPivots.get(0)

        top = highPivot.price
        bottom = lowPivot.price

        difference = top - bottom
        fib050 = top - (difference * fib1)
        fib061 = top - (difference * fib2)

        [fib050, fib061]
    else
        [na, na]

if not na(pivotHigh)
    highPivots.unshift(pivot.new(true, pivotHigh, pHighTime))
    if highPivots.size() > pivLen
        highPivots.pop()
if not na(pivotLow)
    lowPivots.unshift(pivot.new(false, pivotLow, pLowTime))
    if lowPivots.size() > pivLen
        lowPivots.pop()

fib1 = fibArea1
fib2 = fibArea2

[fib05, fib061] = getFibonacciLevels(fib1, fib2)
line05 = plot(fib05, color = gzLineColor, linewidth = 1, style = plot.style_line, display = display.pane)
line061 = plot(fib061, color = gzLineColor, linewidth = 1, style = plot.style_line, display = display.pane)
fill(line05, line061, color = showArea ? gzAreaColor : na)


if barstate.islast
    box.delete(tf1Text)
    //tf1Text := box.new(bar_index - textBack, fib05[textBack / 2], bar_index, fib061[textBack / 2], text = formatTimeframeString(timeframe.period), text_color = textColor, bgcolor = na, border_width = 0, text_size = (textSize == "Auto" ? size.auto : textSize == "Normal" ? size.normal : size.small))



// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/


detectionLength = input.int(14, "Detection Length", group = "General Configuration", tooltip = "This setting determines the amount of candlesticks the indicator will look for trend detection. Higher settings may help the indicator find longer trends, while lower settings will help with finding smaller trends.", display = display.none)
smoothing = input.int(10, "Smoothing", group = "General Configuration", minval = 1, tooltip = "Higher settings will result in longer periods of time required for trend to change direction from bullish to bearish and vice versa.", display = display.none)
EMA1Length = input.int(9, "EMA Lengths          ", group = "General Configuration", inline = "1", display = display.none)
EMA2Length = input.int(21, "", group = "General Configuration", inline = "1", display = display.none)
labelEnabled = input.bool(true, "Labels", group = "General Configuration", inline = "label", display = display.none)
//labelPos     = input.string("Above", "", group = "General Configuration", options = ["Above", "Below"], inline = "label", display = display.none)
//showPreviousLabels = input.bool(false, "Show Previous Labels", group = "General Configuration", display = display.none)
showPreviousLabels = labelEnabled

bearishColor = input.color(#f23646, "Bearish", group = "Colors", inline = "col", display = display.none)
neutralColor = input.color(color.gray, "Neutral", group = "Colors", inline = "col", display = display.none)
bullishColor = input.color(#089981, "Bullish", group = "Colors", inline = "col", display = display.none)

if EMA1Length >= EMA2Length
    runtime.error("First EMA Length must be lower than second EMA Length")

const int minLabelDistance = 0
var int barsSinceLabel = 0

// 0.5, 0.2, 0.3

const float rsiEff = 0.5

const float supertrendFactor = 3.0
const float supertrendEff = 0.2

float emaATRRange = (EMA2Length - EMA1Length) < 20 ? 1.6 : (EMA2Length - EMA1Length) < 50 ? 2 : 3
const float emaCrossEff = 0.3

var label trendLabel = na

f_lin_interpolate(float x0, float x1, float y0, float y1, float x) =>
    y0 + (x - x0) * (y1 - y0) / (x1 - x0)

atr = ta.atr(detectionLength)

curRSI = ta.rsi(close, detectionLength)
curRSI := f_lin_interpolate(15, 85, -100, 100, curRSI)

[supertrend, supDirection] = ta.supertrend(supertrendFactor, detectionLength)
curSupertrend = f_lin_interpolate(-1, 1, -100, 100, -supDirection)

ema1 = ta.ema(close, EMA1Length)
ema2 = ta.ema(close, EMA2Length)
//plot(ema1, color = color.red)
//plot(ema2, color = color.green)
emaDiff = ema1 - ema2
emaDiff := f_lin_interpolate(-atr * emaATRRange, atr * emaATRRange, -100, 100, emaDiff)

totalStrengthRaw = (curRSI * rsiEff) + (curSupertrend * supertrendEff) + (emaDiff * emaCrossEff)
totalStrength = ta.ema(totalStrengthRaw, smoothing)
//log.info(str.tostring(totalStrength))

curColor = color.from_gradient(totalStrength, -100, 0, bearishColor, neutralColor)
if totalStrength > 0
    curColor := color.from_gradient(totalStrength, 15, 85, neutralColor, bullishColor)
barcolor(curColor)

var oldTrendText = "■"
trendText = "■"
if totalStrength < -25
    trendText := "▼"
if totalStrength < -75
    trendText := "▼+"

if totalStrength > 25
    trendText := "▲"
if totalStrength > 75
    trendText := "▲+"

barsSinceLabel += 1

bullishTrendAlert = false
bearishTrendAlert = false
if barstate.isconfirmed
    if showPreviousLabels
        if trendText != oldTrendText and trendText != "■" and barsSinceLabel > minLabelDistance and str.contains(trendText, "+") == false
            barsSinceLabel := 0
            oldTrendText := trendText
            label.new(bar_index, close, trendText, yloc = totalStrength < 0 ? yloc.abovebar : yloc.belowbar, style = totalStrength < 0 ? label.style_label_down : label.style_label_up, color = curColor, textcolor = textColor)
            bullishTrendAlert := (totalStrength > 0)
            bearishTrendAlert := (totalStrength < 0)

alertcondition(bullishTrendAlert, "Bullish Trend", "")
alertcondition(bearishTrendAlert, "Bearish Trend", "")

if barstate.islast and labelEnabled
    label.delete(trendLabel)
    trendLabel := label.new(bar_index, close, trendText, yloc = totalStrength < 0 ? yloc.abovebar : yloc.belowbar, style = totalStrength < 0 ? label.style_label_down : label.style_label_up, color = curColor, textcolor = textColor)

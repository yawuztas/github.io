import pandas as pd
import numpy as np
from utils import calculate_ema, calculate_ma, calculate_fibonacci_levels

def check_ma_hierarchy(data):
    """Check Moving Average hierarchy (20 > 50 > 200)"""
    ma20 = calculate_ma(data['Close'], 20).iloc[-1]
    ma50 = calculate_ma(data['Close'], 50).iloc[-1]
    ma200 = calculate_ma(data['Close'], 200).iloc[-1]

    return ma20 > ma50 > ma200, {
        'MA20': ma20,
        'MA50': ma50,
        'MA200': ma200
    }

def check_fibonacci(data, current_price):
    """Check if price is below 138.2% Fibonacci level"""
    fib_levels = calculate_fibonacci_levels(data)
    return current_price < fib_levels['138.2%'], fib_levels

def calculate_macd(data):
    """Calculate MACD and signal line"""
    ema12 = calculate_ema(data['Close'], 12)
    ema26 = calculate_ema(data['Close'], 26)
    macd = ema12 - ema26
    signal = calculate_ema(macd, 9)
    histogram = macd - signal

    return (macd.iloc[-1] > signal.iloc[-1] and
            histogram.iloc[-1] > histogram.iloc[-2]), {
        'MACD': macd.iloc[-1],
        'Signal': signal.iloc[-1],
        'Histogram': histogram.iloc[-1]
    }

def calculate_rsi(data, periods=14):
    """Calculate RSI"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return 50 <= rsi.iloc[-1] <= 65, rsi.iloc[-1]

def calculate_adx(data, periods=14):
    """Calculate ADX"""
    tr1 = pd.DataFrame(data['High'] - data['Low'])
    tr2 = pd.DataFrame(abs(data['High'] - data['Close'].shift(1)))
    tr3 = pd.DataFrame(abs(data['Low'] - data['Close'].shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis=1, join='inner').max(axis=1)
    atr = tr.rolling(periods).mean()

    plus_dm = data['High'].diff()
    minus_dm = data['Low'].diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0

    plus_di = 100 * (plus_dm.rolling(periods).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(periods).mean() / atr)

    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(periods).mean()

    return 25 <= adx.iloc[-1] <= 40, adx.iloc[-1]
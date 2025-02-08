import yfinance as yf
import pandas as pd
import numpy as np

def fetch_bist100_data():
    """Fetch BIST 100 stocks data"""
    bist100_symbols = [
        "AKBNK.IS", "GARAN.IS", "THYAO.IS", "EREGL.IS", "ASELS.IS", "BIMAS.IS", "KCHOL.IS",
        "SAHOL.IS", "SISE.IS", "TAVHL.IS", "PGSUS.IS", "TUPRS.IS", "HEKTS.IS", "YKBNK.IS",
        "TKFEN.IS", "KRDMD.IS", "FROTO.IS", "AKSEN.IS", "VESTL.IS", "ENJSA.IS", "DOHOL.IS",
        "TTKOM.IS", "TCELL.IS", "EKGYO.IS", "TSKB.IS", "MGROS.IS", "PETKM.IS", "TOASO.IS",
        "ALARK.IS", "ARCLK.IS", "AKSA.IS", "CCOLA.IS", "HALKB.IS", "ICBCT.IS", "IPEKE.IS",
        "ISGYO.IS", "ISDMR.IS", "KARSN.IS", "KONTR.IS", "KOZAA.IS", "KOZAL.IS", "LOGO.IS",
        "MAVI.IS", "NETAS.IS", "OTKAR.IS", "OYAKC.IS", "PRKME.IS", "SASA.IS", "SELEC.IS",
        "SOKM.IS", "TATGD.IS", "TKFEN.IS", "TRGYO.IS", "TSKB.IS", "TTRAK.IS", "ULKER.IS",
        "VAKBN.IS", "VESBE.IS", "YATAS.IS", "ZOREN.IS", "GLYHO.IS", "GUBRF.IS", "ISCTR.IS",
        "KORDS.IS"
    ]

    data = {}
    for symbol in bist100_symbols:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1y")
            if not hist.empty:
                data[symbol] = hist
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

    return data

def calculate_ema(data, periods):
    """Calculate Exponential Moving Average"""
    return data.ewm(span=periods, adjust=False).mean()

def calculate_ma(data, periods):
    """Calculate Simple Moving Average"""
    return data.rolling(window=periods).mean()

def calculate_fibonacci_levels(data):
    """Calculate Fibonacci retracement levels"""
    high = data['High'].max()
    low = data['Low'].min()
    diff = high - low

    levels = {
        'high': high,
        'low': low,
        '38.2%': high - diff * 0.382,
        '50.0%': high - diff * 0.5,
        '61.8%': high - diff * 0.618,
        '138.2%': high + diff * 1.382,
        '161.8%': high + diff * 1.618
    }
    return levels
import streamlit as st
from src.utils import fetch_bist100_data
from src.indicators import (
    check_ma_hierarchy, check_fibonacci, calculate_macd,
    calculate_rsi, calculate_adx
)

def load_css():
    with open("styles/custom.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="BIST 100 Teknik Analiz",
        page_icon="📈",
        layout="wide"
    )

    load_css()

    st.title("BIST 100 Teknik Analiz Platformu")

    # Indicator selection
    st.sidebar.header("Gösterge Seçimi")
    show_ma = st.sidebar.checkbox("MA Hiyerarşisi", value=True)
    show_fib = st.sidebar.checkbox("Fibonacci Seviyeleri", value=True)
    show_macd = st.sidebar.checkbox("MACD", value=True)
    show_rsi = st.sidebar.checkbox("RSI", value=True)
    show_adx = st.sidebar.checkbox("ADX", value=True)

    # Add refresh button
    if st.sidebar.button("Verileri Yenile"):
        st.cache_data.clear()
        st.rerun()  # Updated from experimental_rerun to rerun

    # Fetch data with progress indicator
    with st.spinner("BIST 100 verileri yükleniyor..."):
        stocks_data = fetch_bist100_data()

    if not stocks_data:
        st.error("Veri yüklenemedi. Lütfen daha sonra tekrar deneyin.")
        return

    # Analysis results container
    results = []

    with st.spinner("Teknik analiz yapılıyor..."):
        for symbol, data in stocks_data.items():
            if data.empty:
                continue

            current_price = data['Close'].iloc[-1]
            analysis = {'symbol': symbol, 'price': current_price, 'checks': 0, 'details': []}

            if show_ma:
                ma_check, ma_values = check_ma_hierarchy(data)
                analysis['checks'] += 1 if ma_check else 0
                analysis['details'].append({
                    'name': 'MA Hiyerarşisi',
                    'status': '✅' if ma_check else '❌',
                    'values': ma_values
                })

            if show_fib:
                fib_check, fib_levels = check_fibonacci(data, current_price)
                analysis['checks'] += 1 if fib_check else 0
                analysis['details'].append({
                    'name': 'Fibonacci',
                    'status': '✅' if fib_check else '❌',
                    'values': fib_levels
                })

            if show_macd:
                macd_check, macd_values = calculate_macd(data)
                analysis['checks'] += 1 if macd_check else 0
                analysis['details'].append({
                    'name': 'MACD',
                    'status': '✅' if macd_check else '❌',
                    'values': macd_values
                })

            if show_rsi:
                rsi_check, rsi_value = calculate_rsi(data)
                analysis['checks'] += 1 if rsi_check else 0
                analysis['details'].append({
                    'name': 'RSI',
                    'status': '✅' if rsi_check else '❌',
                    'value': rsi_value
                })

            if show_adx:
                adx_check, adx_value = calculate_adx(data)
                analysis['checks'] += 1 if adx_check else 0
                analysis['details'].append({
                    'name': 'ADX',
                    'status': '✅' if adx_check else '❌',
                    'value': adx_value
                })

            results.append(analysis)

    # Display results
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Güçlü Yükseliş Potansiyeli")
        strong_potentials = [r for r in results if r['checks'] == len(r['details'])]
        if strong_potentials:
            for result in strong_potentials:
                with st.container():
                    st.markdown(f"""
                    <div class="stock-card">
                        <div class="stock-header">{result['symbol'].replace('.IS', '')} - {result['price']:.2f} TL</div>
                        {''.join([f'<div class="indicator success">{detail["name"]}: {detail["status"]}</div>' 
                                for detail in result['details']])}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Şu anda güçlü yükseliş potansiyeli olan hisse bulunmamaktadır.")

    with col2:
        st.subheader("Potansiyel Riskli Hisseler")
        risky_potentials = [r for r in results if 0 < len(r['details']) - r['checks'] <= 2]
        if risky_potentials:
            for result in risky_potentials:
                with st.container():
                    st.markdown(f"""
                    <div class="stock-card">
                        <div class="stock-header">{result['symbol'].replace('.IS', '')} - {result['price']:.2f} TL</div>
                        {''.join([f'<div class="indicator {"success" if detail["status"] == "✅" else "danger"}">{detail["name"]}: {detail["status"]}</div>'
                                for detail in result['details']])}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Şu anda potansiyel riskli hisse bulunmamaktadır.")

if __name__ == "__main__":
    main()
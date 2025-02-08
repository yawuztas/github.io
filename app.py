from flask import Flask, render_template, request, jsonify
from src.utils import fetch_bist100_data
from src.indicators import (
    check_ma_hierarchy, check_fibonacci, calculate_macd,
    calculate_rsi, calculate_adx
)

app = Flask(__name__,
    template_folder='templates',
    static_folder='static'
)

@app.route('/health')
def health_check():
    return jsonify({"status": "ok"})

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        # Get selected indicators
        if request.method == 'POST':
            selected_indicators = request.form.getlist('indicators')
        else:
            selected_indicators = ['ma', 'fib', 'macd', 'rsi', 'adx']  # Default all selected

        # Fetch data with error handling
        try:
            stocks_data = fetch_bist100_data()
            if not stocks_data:
                print("No data returned from fetch_bist100_data")
                return render_template('index.html', error="Veri yüklenemedi. Lütfen daha sonra tekrar deneyin.")
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return render_template('index.html', error="Veri yüklenirken hata oluştu. Lütfen daha sonra tekrar deneyin.")

        # Analysis results container
        results = []

        for symbol, data in stocks_data.items():
            if data.empty:
                continue

            current_price = data['Close'].iloc[-1]
            analysis = {'symbol': symbol, 'price': current_price, 'checks': 0, 'details': []}

            try:
                if 'ma' in selected_indicators:
                    ma_check, ma_values = check_ma_hierarchy(data)
                    analysis['checks'] += 1 if ma_check else 0
                    analysis['details'].append({
                        'name': 'MA Hiyerarşisi',
                        'status': '✅' if ma_check else '❌',
                        'values': ma_values
                    })

                if 'fib' in selected_indicators:
                    fib_check, fib_levels = check_fibonacci(data, current_price)
                    analysis['checks'] += 1 if fib_check else 0
                    analysis['details'].append({
                        'name': 'Fibonacci',
                        'status': '✅' if fib_check else '❌',
                        'values': fib_levels
                    })

                if 'macd' in selected_indicators:
                    macd_check, macd_values = calculate_macd(data)
                    analysis['checks'] += 1 if macd_check else 0
                    analysis['details'].append({
                        'name': 'MACD',
                        'status': '✅' if macd_check else '❌',
                        'values': macd_values
                    })

                if 'rsi' in selected_indicators:
                    rsi_check, rsi_value = calculate_rsi(data)
                    analysis['checks'] += 1 if rsi_check else 0
                    analysis['details'].append({
                        'name': 'RSI',
                        'status': '✅' if rsi_check else '❌',
                        'value': rsi_value
                    })

                if 'adx' in selected_indicators:
                    adx_check, adx_value = calculate_adx(data)
                    analysis['checks'] += 1 if adx_check else 0
                    analysis['details'].append({
                        'name': 'ADX',
                        'status': '✅' if adx_check else '❌',
                        'value': adx_value
                    })

                if analysis['details']:  # Only append if we have any indicators selected
                    results.append(analysis)
            except Exception as e:
                print(f"Error analyzing {symbol}: {str(e)}")
                continue

        # Filter results
        strong_potentials = [r for r in results if r['checks'] == len(r['details'])]
        risky_potentials = [r for r in results if 0 < len(r['details']) - r['checks'] <= 2]

        return render_template('index.html',
                           strong_potentials=strong_potentials,
                           risky_potentials=risky_potentials)
    except Exception as e:
        print(f"Error in index route: {str(e)}")
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5001, debug=True)
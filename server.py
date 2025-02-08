from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import yfinance as yf
from indicators import check_ma_hierarchy, check_fibonacci, calculate_macd, calculate_rsi, calculate_adx
from utils import fetch_bist100_data

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="templates", **kwargs)

    def do_GET(self):
        if self.path.startswith('/api/stocks'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET')
            self.end_headers()

            try:
                # Parse query parameters
                from urllib.parse import urlparse, parse_qs
                query_components = parse_qs(urlparse(self.path).query)
                selected_indicators = query_components.get('indicators', [None])[0]
                selected_indicators = selected_indicators.split(',') if selected_indicators else []

                data = self.fetch_stock_data(selected_indicators)
                if not data:
                    raise Exception("Hiç veri alınamadı")
                self.wfile.write(json.dumps(data, default=str).encode())
            except Exception as e:
                print(f"API Error: {str(e)}")
                error_response = {
                    "error": str(e),
                    "message": "Veri yüklenirken bir hata oluştu"
                }
                self.wfile.write(json.dumps(error_response).encode())
        else:
            super().do_GET()

    def fetch_stock_data(self, selected_indicators):
        """Fetch and analyze stock data for selected indicators only"""
        try:
            # fetch_bist100_data fonksiyonunu kullan
            stocks_data = fetch_bist100_data()
            if not stocks_data:
                print("No data returned from fetch_bist100_data")
                return None

            results = []
            success_count = 0
            total_stocks = len(stocks_data)

            for symbol, hist in stocks_data.items():
                try:
                    if hist.empty:
                        print(f"No data received for {symbol}")
                        continue

                    current_price = hist['Close'].iloc[-1]
                    print(f"Got price for {symbol}: {current_price}")

                    analysis = {
                        'symbol': symbol,
                        'price': float(current_price),
                        'indicators': {}
                    }

                    # Calculate only selected indicators
                    try:
                        if not selected_indicators or 'ma' in selected_indicators:
                            ma_check, _ = check_ma_hierarchy(hist)
                            analysis['indicators']['ma'] = 'true' if ma_check else 'false'

                        if not selected_indicators or 'fib' in selected_indicators:
                            fib_check, _ = check_fibonacci(hist, current_price)
                            analysis['indicators']['fib'] = 'true' if fib_check else 'false'

                        if not selected_indicators or 'macd' in selected_indicators:
                            macd_check, _ = calculate_macd(hist)
                            analysis['indicators']['macd'] = 'true' if macd_check else 'false'

                        if not selected_indicators or 'rsi' in selected_indicators:
                            rsi_check, _ = calculate_rsi(hist)
                            analysis['indicators']['rsi'] = 'true' if rsi_check else 'false'

                        if not selected_indicators or 'adx' in selected_indicators:
                            adx_check, _ = calculate_adx(hist)
                            analysis['indicators']['adx'] = 'true' if adx_check else 'false'

                        results.append(analysis)
                        success_count += 1
                        print(f"Successfully analyzed {symbol}")
                    except Exception as e:
                        print(f"Error calculating indicators for {symbol}: {str(e)}")
                        continue

                except Exception as e:
                    print(f"Error processing {symbol}: {str(e)}")
                    continue

            print(f"Successfully processed {success_count} out of {total_stocks} symbols")
            if success_count == 0:
                raise Exception("Hiçbir hisse verisi alınamadı")

            return results

        except Exception as e:
            print(f"Error in fetch_stock_data: {str(e)}")
            return None

if __name__ == '__main__':
    port = 5000
    print(f"Server starting on port {port}...")
    httpd = HTTPServer(('0.0.0.0', port), Handler)
    httpd.serve_forever()
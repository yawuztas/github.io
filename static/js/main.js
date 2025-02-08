document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(tab.dataset.tab).classList.add('active');
        });
    });

    // Load symbols
    fetch('/api/symbols')
        .then(response => response.json())
        .then(symbols => {
            const select = document.getElementById('symbolSelect');
            symbols.forEach(symbol => {
                const option = document.createElement('option');
                option.value = symbol;
                option.textContent = symbol;
                select.appendChild(option);
            });
            // Load first symbol data
            if (symbols.length > 0) {
                loadStockData(symbols[0]);
            }
        });

    // Symbol selection change
    document.getElementById('symbolSelect').addEventListener('change', (e) => {
        loadStockData(e.target.value);
    });

    // Start scan button
    document.getElementById('startScan').addEventListener('click', () => {
        const filters = {
            MA_Hierarchy: document.getElementById('maHierarchy').checked,
            RSI: document.getElementById('rsi').checked,
            MACD: document.getElementById('macd').checked,
            ADX: document.getElementById('adx').checked,
            PSAR: document.getElementById('psar').checked,
            Fibonacci: document.getElementById('fibonacci').checked
        };

        fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filters)
        })
        .then(response => response.json())
        .then(results => {
            displayResults(results);
        });
    });
});

function loadStockData(symbol) {
    fetch(`/api/stock/${symbol}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }
            updateMetrics(data.indicators);
            createChart(data);
        });
}

function updateMetrics(indicators) {
    const metrics = document.querySelector('.metrics');
    metrics.innerHTML = `
        <div class="metric">
            <div class="label">RSI</div>
            <div class="value">${indicators.rsi.toFixed(2)}</div>
        </div>
        <div class="metric">
            <div class="label">ADX</div>
            <div class="value">${indicators.adx.toFixed(2)}</div>
        </div>
        <div class="metric">
            <div class="label">MA20</div>
            <div class="value">${indicators.ma20.toFixed(2)}</div>
        </div>
        <div class="metric">
            <div class="label">MA50</div>
            <div class="value">${indicators.ma50.toFixed(2)}</div>
        </div>
        <div class="metric">
            <div class="label">MA200</div>
            <div class="value">${indicators.ma200.toFixed(2)}</div>
        </div>
    `;
}

function createChart(data) {
    const dates = data.ohlc.map((_, i) => i);

    const candlestick = {
        x: dates,
        open: data.ohlc.map(d => d.Open),
        high: data.ohlc.map(d => d.High),
        low: data.ohlc.map(d => d.Low),
        close: data.ohlc.map(d => d.Close),
        type: 'candlestick',
        name: 'OHLC'
    };

    const volume = {
        x: dates,
        y: data.volume,
        type: 'bar',
        name: 'Volume',
        yaxis: 'y2'
    };

    const layout = {
        dragmode: 'zoom',
        showlegend: false,
        xaxis: {
            rangeslider: {
                visible: false
            }
        },
        yaxis: {
            title: 'Price'
        },
        yaxis2: {
            title: 'Volume',
            overlaying: 'y',
            side: 'right'
        }
    };

    Plotly.newPlot('chart', [candlestick, volume], layout);
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    if (results.length === 0) {
        resultsDiv.innerHTML = '<p>Kriterlere uyan hisse bulunamadı.</p>';
        return;
    }

    const table = `
        <table>
            <thead>
                <tr>
                    <th>Sembol</th>
                    <th>Son Fiyat</th>
                    <th>RSI</th>
                    <th>ADX</th>
                    <th>MA20</th>
                    <th>MA50</th>
                    <th>MA200</th>
                </tr>
            </thead>
            <tbody>
                ${results.map(stock => `
                    <tr>
                        <td>${stock.symbol}</td>
                        <td>${stock.lastPrice.toFixed(2)}</td>
                        <td>${stock.rsi.toFixed(2)}</td>
                        <td>${stock.adx.toFixed(2)}</td>
                        <td>${stock.ma20.toFixed(2)}</td>
                        <td>${stock.ma50.toFixed(2)}</td>
                        <td>${stock.ma200.toFixed(2)}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    resultsDiv.innerHTML = table;
}

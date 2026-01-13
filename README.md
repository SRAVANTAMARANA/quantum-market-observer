# Quantum Market Observer

This project provides a live XAU/USD (Gold/US Dollar) candlestick chart using the Twelve Data API and TradingView Lightweight Charts. The chart loads by default at `index.html` and includes a toolbar for timeframes and trading tools.

## How to Run

1. Start a local HTTP server in the project directory (e.g., `python3 -m http.server 8080`).
2. Open `index.html` in your browser (e.g., http://localhost:8080/index.html).

## Features

- Live XAU/USD candlestick chart
- Timeframe toolbar (1m, 5m, 15m, 1h, 4h, 1D)
- Trading tools (crosshair, volume, fullscreen, etc.)
- Robust error handling
- Modern dark theme

## Requirements

- Internet connection (for API and CDN)
- Modern web browser

## API Key

The chart uses a demo API key for Twelve Data. For production, replace it with your own key in the HTML file.
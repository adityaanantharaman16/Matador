import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class StockDataCollector:
    def __init__(self, symbol):
        self.stock = yf.Ticker(symbol)
        self.info = self.stock.info

    def get_stock_info(self):
            return {
                    "name": self.info.get("longName"),
                    "symbol": self.stock.ticker,
                    "sector": self.info.get("sector"),
                    "industry": self.info.get("industry"),
                    "price": self.info.get("currentPrice"),
                    "market_cap": self.info.get("marketCap"),
                    "pe_ratio": self.info.get("trailingPE"),
                    "volume": self.info.get("volume"),
                    "52w_high": self.info.get("fiftyTwoWeekHigh"),
                    "52w_low": self.info.get("fiftyTwoWeekLow")
                }

    def plot_price_history(self, period="1y", interval="1d"):
        history = self.stock.history(period=period, interval=interval)

        plt.figure(figsize=(12,6))
        plt.plot(history.index, history['Close'])
        plt.title(f"{self.info.get('longName')} Stock Price - {period}")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.grid(True)
        return plt

    def generate_all_plots(self):
        period = {
            "1d": "1m",
            "5d": "5m",
            "1mo": "1h",
            "6mo":"1d",
            "1y":"1d"
        }

        plots = {}
        for period, interval in period.items():
            plots[period] = self.plot_price_history(period, interval)

        return plots

def main():
    stock = StockDataCollector("AAPL")

    info = stock.get_stock_info()
    print("\nStock Information:")
    for key, value in info.items():
        print(f"{key}: {value}")

    stock.generate_all_plots()
    plt.show()

if __name__ == "__main__":
    main()

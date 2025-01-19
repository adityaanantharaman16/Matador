import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from base_data_collector import BaseDataCollector
from typing import Dict, Any

class StockDataCollector(BaseDataCollector):
    def __init__(self, symbol: str):
        self.stock = yf.Ticker(symbol)
        self.info = self.stock.info

    def get_asset_info(self) -> Dict[str, Any]:
        return {
            "_id": self.stock.ticker,
            "name": self.info.get("longName"),
            "symbol": self.stock.ticker,
            "sector": self.info.get("sector"),
            "industry": self.info.get("industry"),
            "price": self.info.get("currentPrice"),
            "marketCap": self.info.get("marketCap"),
            "peRatio": self.info.get("trailingPE"),
            "volume": self.info.get("volume"),
            "fiftyTwoWeekHigh": self.info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": self.info.get("fiftyTwoWeekLow")
        }

    def plot_price_history(self, period="1y", interval="1d") -> plt.Figure:
        history = self.stock.history(period=period, interval=interval)

        plt.figure(figsize=(12,6))
        plt.plot(history.index, history['Close'])
        plt.title(f"{self.info.get('longName')} Stock Price - {period}")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.grid(True)
        return plt

    def generate_all_plots(self) -> Dict[str, plt.Figure]:
        periods = {
            "1d": "1m",
            "1w": "5m",
            "1m": "1h",
            "3m": "1d",
            "6m": "1d",
            "1y": "1d"
        }

        plots = {}
        for period, interval in periods.items():
            plots[period] = self.plot_price_history(period, interval)
        return plots
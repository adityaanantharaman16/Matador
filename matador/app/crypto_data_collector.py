from pycoingecko import CoinGeckoAPI  # for crypto
import matplotlib.pyplot as plt
import datetime
from base_data_collector import BaseDataCollector
from typing import Dict, Any
class CryptoDataCollector(BaseDataCollector):
    def __init__(self, coin_id: str):
        self.cg = CoinGeckoAPI()
        self.coin_data = self.cg.get_coin_by_id(
            coin_id,
            localization=False,
            tickers=True,
            market_data=True,
            community_data=True,
            developer_data=True
        )

    def get_asset_info(self) -> Dict[str, Any]:
        market_data = self.coin_data['market_data']
        return {
            "_id": self.coin_data['id'],
            "name": self.coin_data['name'],
            "symbol": self.coin_data['symbol'].upper(),
            "description": self.coin_data.get('description', {}).get('en', ''),
            "categories": self.coin_data.get('categories', []),
            "platform": self.coin_data.get('asset_platform_id', 'Native'),
            "currentPriceUSD": market_data['current_price']['usd'],
            "marketCapUSD": market_data['market_cap']['usd'],
            "volume24h": market_data['total_volume']['usd'],
            "circulatingSupply": market_data['circulating_supply'],
            "change24h": market_data['price_change_percentage_24h'],
            "supportedGraphPeriods": ["1d", "1w", "1m", "3m", "6m", "1y"],
            "supportedGraphIntervals": ["1m", "5m", "1h", "1d"]
        }

    def plot_price_history(self, period="1y", interval=None) -> plt.Figure:
        period_days = {
            "1d": 1,
            "1w": 7,
            "1m": 30,
            "3m": 90,
            "6m": 180,
            "1y": 365
        }

        days = period_days.get(period, 365)

        history = self.cg.get_coin_market_chart_range_by_id(
            id=self.coin_data['id'],
            vs_currency='usd',
            from_timestamp=int(datetime.now().timestamp() - (86400 * days)),
            to_timestamp=int(datetime.now().timestamp())
        )

        timestamps = [datetime.fromtimestamp(price[0]/1000) for price in history['prices']]
        prices = [price[1] for price in history['prices']]

        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, prices)
        plt.title(f"{self.coin_data['name']} Price - {period}")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.grid(True)
        return plt

    def generate_all_plots(self) -> Dict[str, plt.Figure]:
        periods = ["1d", "1w", "1m", "3m", "6m", "1y"]
        return {period: self.plot_price_history(period) for period in periods}

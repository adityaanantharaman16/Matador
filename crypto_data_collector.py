from pycoingecko import CoinGeckoAPI  # for crypto
import matplotlib.pyplot as plt
import datetime
class CryptoDataCollector:
    def __init__(self, coin_id):
        self.cg = CoinGeckoAPI()
         # get coin data
        self.coin_data = self.cg.get_coin_by_id(
                coin_id,
                localization=False,
                tickers=True,
                market_data=True,
                community_data=True,
                developer_data=True
            )

    def get_crypto_data(self):
            # get other market data
            market_data = self.coin_data['market_data']
            return {
                "name": self.coin_data['name'],
                "symbol": self.coin_data['symbol'],
                "description": self.coin_data['description']['en'],
                "categories": self.coin_data['categories'],
                "platform": self.coin_data.get('asset_platform_id'), 
                "current_price_usd": market_data['current_price']['usd'],
                 "market_cap_usd": market_data['market_cap']['usd'],
                 "24h_volume": market_data['total_volume']['usd'],
                 "circulating_supply": market_data['circulating_supply'],
                 "24h_change": market_data['price_change_percentage_24h']
            }
    def plot_price_history(self, period="1y"):
        if period == "1d":
            days = 1
        elif period == "1w":
            days = 7
        elif period == "1m":
            days = 30
        elif period == "3m":
            days = 90
        elif period == "6m":
            days = 180
        elif period == "1y":
            days = 365
        else:
            days = 365  # if period is invalid, default to 1 year

        history = self.cg.get_coin_market_chart_range_by_id(
             id=self.coin_data['id'],
             vs_currency='usd',
             from_timestamp=datetime.datetime.now().timestamp() - (86400 * days),
                to_timestamp=datetime.datetime.now().timestamp()
         )
        timestamps = [datetime.datetime.fromtimestamp(price[0] / 1000) for price in history['prices']]
        prices = [price[1] for price in history['prices']]

        plt.figure(figsize=(12,6))
        plt.plot(timestamps, prices, label = 'Close Price')
        plt.title(f"{self.coin_data['name']} Price - {period}")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.grid(True)
        return plt
    def generate_all_plots(self):
        periods = ["1d", "1w", "1m", "3m", "6m", "1y"]
        plots = {}
        for period in periods:
            plots[period] = self.plot_price_history(period)
        return plots
    
def main():
    crypto = CryptoDataCollector("bitcoin")
    info = crypto.get_crypto_data()
    print("\nCrypto Information:")
    for key, value in info.items():
        print(f"{key}: {value}")
    crypto.generate_all_plots()
    plt.show()

if __name__ == "__main__":
    main()
       
    




        
    
        
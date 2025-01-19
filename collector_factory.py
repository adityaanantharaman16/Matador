from typing import Union

from stock_data_collector import StockDataCollector
from crypto_data_collector import CryptoDataCollector
class AssetCollectorFactory:
    @staticmethod
    def get_collector(asset_type: str, symbol: str) -> Union[StockDataCollector, CryptoDataCollector]:
        """
        Factory method to create appropriate collector based on asset type.

        Args:
            asset_type (str): Type of asset ("stock" or "crypto")
            symbol (str): Symbol/identifier for the asset

        Returns:
            Union[StockDataCollector, CryptoDataCollector]: Appropriate data collector instance

        Raises:
            ValueError: If asset type is not supported
        """
        collectors = {
            "stock": StockDataCollector,
            "crypto": CryptoDataCollector
        }

        collector_class = collectors.get(asset_type.lower())
        if not collector_class:
            raise ValueError(
                f"Unsupported asset type: {asset_type}. "
                f"Supported types are: {', '.join(collectors.keys())}"
            )

        return collector_class(symbol)
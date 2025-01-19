from abc import ABC, abstractmethod
from typing import Dict, Any
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
class BaseDataCollector(ABC):
    @abstractmethod
    def get_asset_info(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def plot_price_history(self, period: str) -> plt.Figure:
        pass

    @abstractmethod
    def generate_all_plots(self) -> Dict[str, plt.Figure]:
        pass

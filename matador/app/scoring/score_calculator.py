from datetime import datetime, timedelta
import numpy as np
from typing import List, Dict, Any

class ScoreCalculator:
    @staticmethod
    def calculate_performance_score(
            current_price: float,
            pitch_price: float,
            market_return: float,
            price_history: List[float]
    ) -> float:
        # Calculate return percentage
        return_pct = ((current_price - pitch_price) / pitch_price) * 100

        # Compare to market return
        market_comparison = return_pct - market_return

        # Calculate price momentum using recent price history
        momentum = ScoreCalculator._calculate_momentum(price_history)

        # Combine metrics with weights
        score = (
                return_pct * 0.5 +
                market_comparison * 0.3 +
                momentum * 0.2
        )

        # Normalize to 0-100 scale
        return max(0, min(100, score))

    @staticmethod
    def calculate_engagement_score(
            likes: int,
            comments: int,
            shares: int,
            saves: int,
            hours_since_creation: float
    ) -> float:
        # Calculate rates per hour
        like_rate = likes / max(1, hours_since_creation)
        comment_rate = comments / max(1, hours_since_creation)
        share_rate = shares / max(1, hours_since_creation)
        save_rate = saves / max(1, hours_since_creation)

        # Combine metrics with weights
        score = (
                        like_rate * 0.4 +
                        comment_rate * 0.3 +
                        share_rate * 0.2 +
                        save_rate * 0.1
                ) * 100

        return max(0, min(100, score))

    @staticmethod
    def calculate_credibility_score(
            author_karma: float,
            success_rate: float,
            pitch_count: int,
            days_active: int
    ) -> float:
        # Calculate activity consistency
        activity_rate = pitch_count / max(1, days_active)

        # Normalize karma to 0-100 scale
        normalized_karma = min(100, author_karma / 10)

        # Combine metrics with weights
        score = (
                normalized_karma * 0.4 +
                success_rate * 0.4 +
                activity_rate * 0.2
        )

        return max(0, min(100, score))

    @staticmethod
    def calculate_market_relevance(
            trading_volume: float,
            avg_volume: float,
            sector_performance: float,
            market_sentiment: float
    ) -> float:
        # Calculate volume ratio
        volume_ratio = trading_volume / max(1, avg_volume)

        # Combine metrics with weights
        score = (
                        volume_ratio * 0.4 +
                        abs(sector_performance) * 0.3 +
                        market_sentiment * 0.3
                ) * 100

        return max(0, min(100, score))

    @staticmethod
    def _calculate_momentum(price_history: List[float]) -> float:
        if len(price_history) < 2:
            return 0

        # Calculate price changes
        changes = np.diff(price_history)

        # Calculate exponentially weighted momentum
        weights = np.exp(np.linspace(-1, 0, len(changes)))
        weighted_changes = changes * weights

        return np.sum(weighted_changes) / np.sum(weights)

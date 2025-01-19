from datetime import datetime
from typing import Dict, Any, Optional
from .scoring_models import (
    ScoreWeights,
    PerformanceMetrics,
    EngagementMetrics,
    CredibilityMetrics,
    MarketMetrics,
    ContentScore
)
from .score_calculator import ScoreCalculator
from collector_factory import AssetCollectorFactory

class ContentScorer:
    def __init__(self):
        self.weights = ScoreWeights()
        self.calculator = ScoreCalculator()

    async def calculate_pitch_score(
            self,
            pitch_data: Dict[str, Any],
            user_karma: Dict[str, Any]
    ) -> ContentScore:
        # Get asset data
        asset_type = "crypto" if "crypto" in pitch_data else "stock"
        symbol = pitch_data.get("crypto" if asset_type == "crypto" else "stock")
        collector = AssetCollectorFactory.get_collector(asset_type, symbol)
        asset_info = collector.get_asset_info()

        # Calculate component scores
        performance_score = await self._calculate_performance_score(
            pitch_data,
            asset_info
        )

        engagement_score = await self._calculate_engagement_score(
            pitch_data
        )

        credibility_score = await self._calculate_credibility_score(
            pitch_data,
            user_karma
        )

        market_score = await self._calculate_market_score(
            asset_info
        )

        # Calculate total score
        total_score = (
                performance_score * self.weights.performance_weight +
                engagement_score * self.weights.engagement_weight +
                credibility_score * self.weights.credibility_weight +
                market_score * self.weights.market_relevance_weight
        )

        return ContentScore(
            _id=pitch_data["_id"],
            total_score=total_score,
            performance_score=performance_score,
            engagement_score=engagement_score,
            credibility_score=credibility_score,
            market_relevance_score=market_score
        )

    async def _calculate_performance_score(
            self,
            pitch_data: Dict[str, Any],
            asset_info: Dict[str, Any]
    ) -> float:
        current_price = asset_info["currentPriceUSD"]
        pitch_price = pitch_data["pitchPrice"]

        # Get market data using your data collectors
        market_return = 0  # You'll need to implement market return calculation
        price_history = []  # You'll need to implement price history retrieval

        return self.calculator.calculate_performance_score(
            current_price,
            pitch_price,
            market_return,
            price_history
        )

    async def _calculate_engagement_score(
            self,
            pitch_data: Dict[str, Any]
    ) -> float:
        created_at = datetime.fromisoformat(pitch_data["createdAt"].rstrip('Z'))
        hours_since_creation = (datetime.utcnow() - created_at).total_seconds() / 3600

        return self.calculator.calculate_engagement_score(
            pitch_data.get("likes", 0),
            len(pitch_data.get("comments", [])),
            pitch_data.get("shares", 0),
            pitch_data.get("saves", 0),
            hours_since_creation
        )

    async def _calculate_credibility_score(
            self,
            pitch_data: Dict[str, Any],
            user_karma: Dict[str, Any]
    ) -> float:
        is_crypto = "crypto" in pitch_data
        karma = user_karma["cryptoKarma"] if is_crypto else user_karma["stockKarma"]
        pitch_count = user_karma["totalCryptoPitches" if is_crypto else "totalStockPitches"]

        # You'll need to implement these calculations
        success_rate = 0
        days_active = 30  # Default value, implement actual calculation

        return self.calculator.calculate_credibility_score(
            karma,
            success_rate,
            pitch_count,
            days_active
        )

    async def _calculate_market_score(
            self,
            asset_info: Dict[str, Any]
    ) -> float:
        # You'll need to implement these calculations using your data collectors
        trading_volume = asset_info.get("volume24h", 0)
        avg_volume = 0  # Implement average volume calculation
        sector_performance = 0  # Implement sector performance calculation
        market_sentiment = 0  # Implement market sentiment calculation

        return self.calculator.calculate_market_relevance(
            trading_volume,
            avg_volume,
            sector_performance,
            market_sentiment
        )
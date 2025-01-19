from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class ScoreWeights(BaseModel):
    performance_weight: float = 0.4
    engagement_weight: float = 0.3
    credibility_weight: float = 0.2
    market_relevance_weight: float = 0.1

class PerformanceMetrics(BaseModel):
    return_percentage: float
    market_comparison: float
    price_momentum: float

class EngagementMetrics(BaseModel):
    like_rate: float
    comment_count: int
    share_count: int
    save_count: int

class CredibilityMetrics(BaseModel):
    author_karma: float
    success_rate: float
    activity_consistency: float

class MarketMetrics(BaseModel):
    trading_volume: float
    market_sentiment: float
    sector_performance: float

class ContentScore(BaseModel):
    pitch_id: str = Field(alias="_id")
    total_score: float
    performance_score: float
    engagement_score: float
    credibility_score: float
    market_relevance_score: float
    calculated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True)
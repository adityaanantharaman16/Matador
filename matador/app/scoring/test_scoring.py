# matador/app/scoring/test_scoring.py
import pytest
from score_calculator import ScoreCalculator
import numpy as np
from datetime import datetime, timedelta

pytestmark = pytest.mark.asyncio

@pytest.fixture
def sample_price_history():
    return [145.0, 148.0, 152.0, 155.0, 160.0]

@pytest.fixture
def test_calculator():
    return ScoreCalculator()

@pytest.fixture
def mock_pitch_data():
    return {
        "_id": "test_pitch_1",
        "user": "test_user",
        "stock": "AAPL",
        "thesis": "Test thesis",
        "pitchPrice": 150.00,
        "createdAt": datetime.utcnow().isoformat(),
        "likes": 10,
        "comments": ["comment1", "comment2"],
        "shares": 5
    }

async def test_performance_score_calculation(test_calculator, sample_price_history):
    """Test the performance score calculation."""
    # Calculate actual percentage return
    start_price = 150.00
    end_price = 160.00
    market_return = 3.0

    return_pct = ((end_price - start_price) / start_price) * 100  # Should be 6.67%
    outperformance = return_pct - market_return  # Should be 3.67%

    score = test_calculator.calculate_performance_score(
        current_price=end_price,
        pitch_price=start_price,
        market_return=market_return,
        price_history=sample_price_history
    )

    # Print debug information
    print(f"\nReturn %: {return_pct}")
    print(f"Market Return: {market_return}")
    print(f"Outperformance: {outperformance}")
    print(f"Final Score: {score}")

    assert isinstance(score, (int, float))
    assert 0 <= score <= 100
    assert score > 20  # Adjusted threshold based on your scoring algorithm

@pytest.mark.performance
async def test_engagement_score_calculation(test_calculator):
    """Test the engagement score calculation."""
    # Test with high engagement
    high_score = test_calculator.calculate_engagement_score(
        likes=100,
        comments=20,
        shares=50,
        saves=30,
        hours_since_creation=24.0
    )

    # Test with low engagement
    low_score = test_calculator.calculate_engagement_score(
        likes=1,
        comments=0,
        shares=0,
        saves=0,
        hours_since_creation=24.0
    )

    print(f"\nHigh Engagement Score: {high_score}")
    print(f"Low Engagement Score: {low_score}")

    assert high_score > low_score
    assert 0 <= high_score <= 100
    assert 0 <= low_score <= 100

@pytest.mark.performance
async def test_feed_performance(async_client, mock_pitch_data):
    """Test the performance of feed generation."""
    # First, create some test data
    pitches = []
    for i in range(10):
        pitch = mock_pitch_data.copy()
        pitch["_id"] = f"test_pitch_{i}"
        pitches.append(pitch)

    # Time the feed generation
    start_time = datetime.utcnow()

    try:
        response = await async_client.get(
            "/feed/test_user/for-you",
            params={
                "page": 1,
                "page_size": 20
            }
        )
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()

        print(f"\nFeed Generation Time: {duration} seconds")

        assert response.status_code == 200
        assert duration < 1.0  # Should respond within 1 second

    except Exception as e:
        print(f"Error during feed generation: {str(e)}")
        raise

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
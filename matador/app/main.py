from fastapi import Query, Path, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from database import app
from typing import Dict, Any, List, Optional
from scoring.scoring_models import ContentScore
from enum import Enum



from crud import (
    users_crud,
    stocks_crud,
    crypto_crud,
    stock_pitches_crud,
    crypto_pitches_crud,
    comments_crud
)
from models import (
    UserResponse,
    TestUserResponse,
    TestUsersResponse
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/test/user", response_model=TestUserResponse)
async def create_test_user():
    test_user = {
        "name": "Test User",
        "email": "test@example.com",
        "password_hash": "test_hash",
        "bio": "This is a test user",
        "profilePicture": None,
        "stockKarma": 0,
        "cryptoKarma": 0,
        "totalStockPitches": 0,
        "totalCryptoPitches": 0,
        "followers": [],
        "following": [],
        "stockPitches": [],
        "cryptoPitches": [],
        "likedStockPitches": [],
        "likedCryptoPitches": []
    }

    created_user = await users_crud.create(test_user)
    return {
        "message": "Test user created",
        "user": created_user
    }


@app.get("/test/users", response_model=TestUsersResponse)
async def get_all_test_users():
    users = await users_crud.get_all()
    return {
        "total_users": len(users),
        "users": users
    }


@app.post("/test/user/create")
async def create_custom_user(
        user_id: str,
        name: str,
        bio: str = "New investor",
        stockKarma: float = 0,
        cryptoKarma: float = 0
):
    user_data = {
        "_id": user_id,
        "name": name,
        "profilePicture": "https://example.com/default.jpg",
        "bio": bio,
        "followers": [],
        "following": [],
        "stockKarma": stockKarma,
        "totalStockLikes": 0,
        "totalStockPitches": 0,
        "cryptoKarma": cryptoKarma,
        "totalCryptoLikes": 0,
        "totalCryptoPitches": 0,
        "stockPitches": [],
        "likedStockPitches": [],
        "cryptoPitches": [],
        "likedCryptoPitches": []
    }

    created_user = await users_crud.create(user_data)
    return {"message": "User created", "user": created_user}


@app.get("/test/user/{user_id}")
async def get_user_by_id(user_id: str):
    user = await users_crud.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Stock endpoints
from collector_factory import AssetCollectorFactory


@app.get("/api/stocks/{symbol}")
async def get_stock_info(symbol: str):
    """
    Get detailed information for a specific stock
    """
    try:
        collector = AssetCollectorFactory.get_collector("stock", symbol)
        return collector.get_asset_info()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching stock data: {str(e)}"
        )

@app.get("/api/stocks/{symbol}/price_history")
async def get_stock_history(
        symbol: str,
        period: str = "1y",
        interval: str = "1d"
):
    """
    Get price history for a stock
    """
    try:
        collector = AssetCollectorFactory.get_collector("stock", symbol)
        figure = collector.plot_price_history(period, interval)
        return collector.plot_price_history(period, interval)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching stock history: {str(e)}"
        )

# Crypto endpoints
@app.get("/api/crypto/{coin_id}")
async def get_crypto_info(coin_id: str):
    """
    Get detailed information for a specific cryptocurrency
    """
    try:
        collector = AssetCollectorFactory.get_collector("crypto", coin_id)
        return collector.get_asset_info()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching crypto data: {str(e)}"
        )

@app.get("/api/crypto/{coin_id}/price_history")
async def get_crypto_history(
        coin_id: str,
        period: str = "1y"
):
    """
    Get price history for a cryptocurrency
    """
    try:
        collector = AssetCollectorFactory.get_collector("crypto", coin_id)
        return collector.plot_price_history(period)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching crypto history: {str(e)}"
        )
# Feed endpoints
@app.get(
    "/feed/{user_id}/for-you",
    response_model=List[Dict[str, Any]]
)
async def get_personalized_feed(
        user_id: str = Path(
            ...,
            title="User ID",
            description="The ID of the user to generate feed for"
        ),
        page: int = Query(
            default=1,
            ge=1,
            title="Page Number",
            description="Page number for pagination"
        ),
        page_size: int = Query(
            default=20,
            ge=1,
            le=100,
            title="Page Size",
            description="Number of items per page"
        ),
        min_score: float = Query(
            default=0.0,
            ge=0.0,
            le=100.0,
            title="Minimum Score",
            description="Minimum score threshold for pitches"
        ),
        asset_type: Optional[str] = Query(
            default=None,
            title="Asset Type",
            description="Filter by asset type (stock or crypto)"
        )
):
    """
    Get personalized feed for a user with optional filtering and pagination.
    """
    try:
        # Validate user exists
        user = await users_crud.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # Calculate skip for pagination
        skip = (page - 1) * page_size

        # Initialize empty lists for pitches
        stock_pitches = []
        crypto_pitches = []

        # Fetch pitches based on asset_type filter
        if asset_type in [None, 'stock']:
            stock_pitches = await stock_pitches_crud.get_top_scored(
                limit=page_size,
                skip=skip,
                min_score=min_score
            )

        if asset_type in [None, 'crypto']:
            crypto_pitches = await crypto_pitches_crud.get_top_scored(
                limit=page_size,
                skip=skip,
                min_score=min_score
            )

        # Combine and sort results
        all_pitches = stock_pitches + crypto_pitches
        sorted_pitches = sorted(
            all_pitches,
            key=lambda x: x['score']['total_score'],
            reverse=True
        )

        return sorted_pitches[:page_size]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating feed: {str(e)}"
        )


@app.get(
    "/pitch/{pitch_id}/score",
    response_model=ContentScore
)
async def get_pitch_score(
        pitch_id: str = Path(
            ...,
            title="Pitch ID",
            description="The ID of the pitch to get score for"
        ),
        recalculate: bool = Query(
            default=False,
            title="Recalculate Score",
            description="Whether to recalculate the score"
        ),
        background_tasks: BackgroundTasks = None
):
    """
    Get score for a specific pitch with optional recalculation.
    """
    try:
        # Determine pitch type and get appropriate CRUD instance
        if pitch_id.startswith('stock_pitch_'):
            crud_instance = stock_pitches_crud
        elif pitch_id.startswith('crypto_pitch_'):
            crud_instance = crypto_pitches_crud
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid pitch ID format"
            )

        # Get pitch
        pitch = await crud_instance.get_by_id(pitch_id)
        if not pitch:
            raise HTTPException(
                status_code=404,
                detail="Pitch not found"
            )

        if recalculate:
            # Get user karma
            user_karma = await users_crud.get_by_id(pitch['user'])
            if not user_karma:
                raise HTTPException(
                    status_code=404,
                    detail="Pitch author not found"
                )

            # Calculate new score
            score = await crud_instance.content_scorer.calculate_pitch_score(
                pitch,
                user_karma
            )

            # Update score in background if background_tasks provided
            if background_tasks:
                background_tasks.add_task(
                    crud_instance.update,
                    pitch_id,
                    {'score': score.model_dump()}
                )
            else:
                # Update immediately if no background_tasks
                await crud_instance.update(
                    pitch_id,
                    {'score': score.model_dump()}
                )

            return score

        # Return existing score
        if 'score' not in pitch:
            raise HTTPException(
                status_code=404,
                detail="Score not found for pitch"
            )

        return ContentScore(**pitch['score'])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting pitch score: {str(e)}"
        )


@app.post(
    "/admin/scores/recalculate",
    response_model=Dict[str, Any]
)
async def recalculate_all_scores(
        asset_type: Optional[str] = Query(
            default=None,
            title="Asset Type",
            description="Type of pitches to recalculate scores for"
        ),
        background_tasks: BackgroundTasks = None
):
    """
    Admin endpoint to recalculate all scores with optional filtering.
    """
    try:
        update_count = 0

        async def update_scores(crud_instance):
            return await crud_instance.update_scores()

        if asset_type in [None, 'stock']:
            if background_tasks:
                background_tasks.add_task(update_scores, stock_pitches_crud)
                update_count += 1  # Count task instead of updates
            else:
                stock_count = await update_scores(stock_pitches_crud)
                update_count += stock_count

        if asset_type in [None, 'crypto']:
            if background_tasks:
                background_tasks.add_task(update_scores, crypto_pitches_crud)
                update_count += 1  # Count task instead of updates
            else:
                crypto_count = await update_scores(crypto_pitches_crud)
                update_count += crypto_count

        return {
            "message": (
                "Score update tasks queued"
                if background_tasks
                else "Score update complete"
            ),
            "update_count": update_count,
            "mode": "background" if background_tasks else "synchronous"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating scores: {str(e)}"
        )

# matador/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import app, db
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
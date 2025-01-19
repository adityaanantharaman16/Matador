from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    profilePicture: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    password_hash: str
    stockKarma: float = 0
    cryptoKarma: float = 0
    totalStockPitches: int = 0
    totalCryptoPitches: int = 0
    followers: List[str] = []
    following: List[str] = []
    stockPitches: List[str] = []
    cryptoPitches: List[str] = []
    likedStockPitches: List[str] = []
    likedCryptoPitches: List[str] = []

    model_config = ConfigDict(populate_by_name=True)

class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: EmailStr
    profilePicture: Optional[str] = None
    bio: Optional[str] = None
    stockKarma: float
    cryptoKarma: float
    totalStockPitches: int
    totalCryptoPitches: int

    model_config = ConfigDict(populate_by_name=True)

class TestUserResponse(BaseModel):
    message: str
    user: UserResponse

    model_config = ConfigDict(populate_by_name=True)

class TestUsersResponse(BaseModel):
    total_users: int
    users: List[UserResponse]

    model_config = ConfigDict(populate_by_name=True)
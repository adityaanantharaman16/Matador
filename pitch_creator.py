from typing import Dict, Any
from datetime import datetime
class PitchCreator:
    def create_stock_pitch(
            self,
            user_id: str,
            symbol: str,
            thesis: str,
            pitch_price: float
    ) -> Dict[str, Any]:
        """Creates a stock pitch document according to MongoDB schema"""
        return {
            "_id": f"stock_pitch_{user_id}_{symbol}_{int(datetime.now().timestamp())}",
            "user": user_id,
            "stock": symbol,
            "thesis": thesis,
            "pitchPrice": pitch_price,
            "returnPercentage": 0.0,  # Initial return percentage
            "likes": 0,
            "comments": [],
            "createdAt": datetime.now().isoformat() + "Z"
        }

    def create_crypto_pitch(
            self,
            user_id: str,
            symbol: str,
            thesis: str,
            pitch_price: float
    ) -> Dict[str, Any]:
        """Creates a crypto pitch document according to MongoDB schema"""
        return {
            "_id": f"crypto_pitch_{user_id}_{symbol}_{int(datetime.now().timestamp())}",
            "user": user_id,
            "crypto": symbol,
            "thesis": thesis,
            "pitchPrice": pitch_price,
            "returnPercentage": 0.0,  # Initial return percentage
            "likes": 0,
            "comments": [],
            "shares": 0,
            "createdAt": datetime.now().isoformat() + "Z"
        }
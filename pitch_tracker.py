from typing import Dict

class KarmaSystem:
    """Handles user karma calculations and updates based on the schema"""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self._stock_karma = 0
        self._crypto_karma = 0
        self._total_stock_likes = 0
        self._total_crypto_likes = 0
        self._total_stock_pitches = 0
        self._total_crypto_pitches = 0

    def update_karma(
            self,
            is_crypto: bool,
            return_percentage: float,
            likes_delta: int = 0
    ):
        """Updates karma based on performance and engagement"""
        # Performance-based karma (preserved from original scoring logic)
        karma_change = min(100, (return_percentage / 20) * 100)

        # Add likes-based karma
        karma_change += likes_delta * 5  # 5 karma points per like

        if is_crypto:
            self._crypto_karma += karma_change
            self._total_crypto_likes += likes_delta
            self._total_crypto_pitches += 1
        else:
            self._stock_karma += karma_change
            self._total_stock_likes += likes_delta
            self._total_stock_pitches += 1

    def get_user_karma(self) -> Dict:
        """Returns user karma information according to schema"""
        return {
            "stockKarma": self._stock_karma,
            "totalStockLikes": self._total_stock_likes,
            "totalStockPitches": self._total_stock_pitches,
            "cryptoKarma": self._crypto_karma,
            "totalCryptoLikes": self._total_crypto_likes,
            "totalCryptoPitches": self._total_crypto_pitches
        }
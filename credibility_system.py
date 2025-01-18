import numpy as np
class CredibilitySystem:
    TIERS = {
        'bronze': {'min_score': 0, 'color_code': '#CD7F32'},
        'silver': {'min_score': 100, 'color_code': '#C0C0C0'},
        'gold': {'min_score': 250, 'color_code': '#FFD700'},
        'platinum': {'min_score': 500, 'color_code': '#E5E4E2'},
        'diamond': {'min_score': 1000, 'color_code': '#B9F2FF'}
    }

    WEIGHTS = {
        'return_percentage': 0.4,
        'success_rate': 0.3,
        'consistency': 0.15,
        'risk_management': 0.15
    }

    def __init__(self, user_id):
        self.user_id = user_id
        self.total_score = 0
        self.pitch_history = []
        self.current_tier = 'bronze'

    def calculate_return_score(self, returns):
        return min(100, (returns / 20) * 100)

    def calculate_success_rate_score(self, successful_pitches, total_pitches):
        if total_pitches == 0:
            return 0
        success_rate = (successful_pitches / total_pitches) * 100
        return success_rate

    def calculate_consistency_score(self, monthly_returns):
        if not monthly_returns:
            return 0

        std_dev = np.std(monthly_returns)
        consistency_score = max(0, 100 * (1 - (std_dev / 30)))
        return consistency_score

    def calculate_risk_management_score(self, pitches):
        if not pitches:
            return 0

        pitches_with_stops = sum(1 for pitch in pitches if pitch.get('stop_loss'))
        pitches_with_targets = sum(1 for pitch in pitches if pitch.get('target_price'))

        risk_score = (
                (pitches_with_stops / len(pitches) * 50) +
                (pitches_with_targets / len(pitches) * 50)
        )
        return risk_score

    def update_user_score(self, performance_metrics):
        scores = {
            'return percentage': self.calculate_return_score(
                performance_metrics['average_return']
            ),
            'success_rate': self.calculate_success_rate_score(
                performance_metrics['successful_pitches'],
                performance_metrics['total_pitches']
            ),
            'consistency': self.calculate_consistency_score(
                performance_metrics['monthly_returns']
            ),
            'risk_management': self.calculate_risk_management_score(
                performance_metrics['pitches']
            )
        }

        self.total_score = sum(
            scores[metric] * weight
            for metric, weight in self.WEIGHTS.items()
        )

        self.update_tier()

        return {
            'user_id': self.user_id,
            'total_score': self.total_score,
            'tier': self.current_tier,
            'detailed_scores': scores
        }

    def update_tier(self):
        """Update user's tier based on their total score"""
        for tier, requirements in sorted(
                self.TIERS.items(),
                key=lambda x: x[1]['min_score'],
                reverse=True
        ):
            if self.total_score >= requirements['min_score']:
                self.current_tier = tier
                break

    def get_pitch_weight(self):
        tier_multipliers = {
            'bronze': 1.0,
            'silver': 1.2,
            'gold': 1.5,
            'platinum': 2.0,
            'diamond': 2.5
        }
        return tier_multipliers.get(self.current_tier, 1.0)

    def get_badge_info(self):
        return {
            'tier': self.current_tier,
            'color': self.TIERS[self.current_tier]['color_code'],
            'score': self.total_score,
            'next_tier': self.get_next_tier_info()
        }

    def get_next_tier_info(self):
        current_tier_score = self.TIERS[self.current_tier]['min_score']

        tiers = sorted(self.TIERS.items(), key=lambda x: x[1]['min_score'])
        for tier, requirements in tiers:
            if requirements['min_score'] > current_tier_score:
                return {
                    'next_tier': tier,
                    'points_needed': requirements['min_score'] - self.total_score
                }

            return None



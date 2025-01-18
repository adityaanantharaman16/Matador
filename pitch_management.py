from datetime import datetime
import numpy as np
from typing import Dict, List, Optional
from credibility_system import CredibilitySystem

class PitchTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.pitches: Dict = {}
        self.credibility_system = CredibilitySystem(user_id)

    def create_pitch(self, symbol, entry_price, thesis,
                     timestamp, target_price=None, stop_loss=None):
        pitch_id = f"{self.user_id}_{symbol}_{timestamp}"

        self.pitches[pitch_id] = {
            'symbol': symbol,
            'entry_price': entry_price,
            'thesis': thesis,
            'timestamp': timestamp,
            'target_price': target_price,
            'stop_loss': stop_loss,
            'status': 'active',
            'performance_history': []
        }
        return pitch_id

    def calculate_pitch_performance(self, pitch_id: str, current_price: float) -> Dict:
        pitch = self.pitches.get(pitch_id)
        if not pitch:
            raise ValueError("Pitch not found")

        performance = {
            'absolute_return': current_price - pitch['entry_price'],
            'percentage_return': ((current_price - pitch['entry_price'])
                                  / pitch['entry_price']) * 100,
            'timetamp': datetime.now(),
            'current_price': current_price,
            'weighted_return': ((current_price - pitch['entry_price']) / pitch['entry_price'])
                               * 100 * pitch['weight']
        }

        if pitch['target_price']:
            performance['target_achievement'] = (
                    (current_price - pitch['entry_price']) / (pitch['target_price']
                                                              - pitch['entry_price']) * 100)

        pitch['performance_history'].append(performance)
        self._update_user_credibility()

        return performance

    def get_user_performance_metrics(self) -> Dict:
        total_pitches = len(self.pitches)

        if total_pitches == 0:
            return self._empty_performance_metrics()

        successful_pitches = sum(1 for pitch in self.pitches.values()
                                 if pitch['performance_history'] and
                                 pitch['performance_history'][-1]['percentage_return'] > 0)

        monthly_returns = self._calculate_monthly_returns()

        metrics = {
            'total_pitches': total_pitches,
            'successful_pitches':successful_pitches,
            'success_rate': (successful_pitches / total_pitches * 100),
            'average_return': self._calculate_average_return(),
            'monthly_returns': monthly_returns,
            'user_id': self.user_id,
            'pitches': self.pitches
        }
        return metrics

    def _empty_performance_metrics(self) -> Dict:
        return {
            'total_pitches': 0,
            'successful_pitches': 0,
            'success_rate': 0,
            'average_return': 0,
            'monthly_returns': [],
            'user_id': self.user_id,
            'pitches': {}
        }

    def _calculate_monthly_returns(self) -> List[float]:
        monthly_returns = []
        for pitch in self.pitches.values():
            if not pitch['performance_history']:
                continue

            returns = [perf['percentage_return'] for perf in pitch['performance_history']]
            monthly_returns.extend(returns)
        return monthly_returns

    def _calculate_average_return(self) -> float:
        total_weighted_return = 0
        total_weight = 0

        for pitch in self.pitches.values():
            if not pitch['performance history']:
                continue
            weight = pitch['weight']
            return_val = pitch['performance_history'][-1]['percentage_return']
            total_weighted_return += return_val * weight
            total_weight += weight

        return total_weighted_return / total_weight if total_weight > 0 else 0

    def _update_user_credibility(self):
        metrics = self.get_user_performance_metrics()
        self.credibility_system.update_user_score(metrics)

        def get_user_credibility_info(self) -> Dict:
            return {
                'badge_info': self.credibility_system.get_badge_info(),
                'performance_metrics': self.get_user_performance_metrics(),
                'current_tier': self.credibility_system.current_tier,
                'total_score': self.credibility_system.total_score
            }
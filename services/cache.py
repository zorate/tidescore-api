from datetime import datetime
from models.score import Score

class CacheService:
    @staticmethod
    def get_cached_score(user_id, force_refresh=False):
        """Get cached score or recalculate if needed"""
        cached_score = Score.find_by_user_id(user_id)
        
        if not cached_score or force_refresh or not Score.is_valid(cached_score):
            return None, 'recalculate'
        
        return cached_score, 'cached'
    
    @staticmethod
    def refresh_score(user_id):
        """Force refresh of score"""
        from services.scoring import ScoringService
        score_data = ScoringService.calculate_score(user_id)
        return Score.create_or_update(user_id, score_data)
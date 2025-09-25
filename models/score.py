from datetime import datetime, timedelta
from models import scores_collection
from config import Config

class Score:
    @staticmethod
    def create_or_update(user_id, score_data):
        """Create or update a score with 30-day validity"""
        valid_until = datetime.utcnow() + timedelta(days=Config.SCORE_CACHE_DAYS)
        
        score_doc = {
            'user_id': user_id,
            'score': score_data.get('score'),
            'status': score_data.get('status'),
            'advice': score_data.get('advice'),
            'breakdown': score_data.get('breakdown', {}),
            'last_calculated': datetime.utcnow(),
            'valid_until': valid_until,
            'data_points_used': score_data.get('data_points_used', 0)
        }
        
        # Upsert the score
        result = scores_collection.update_one(
            {'user_id': user_id},
            {'$set': score_doc},
            upsert=True
        )
        
        return scores_collection.find_one({'user_id': user_id})

    @staticmethod
    def find_by_user_id(user_id):
        """Find score by user ID"""
        return scores_collection.find_one({'user_id': user_id})

    @staticmethod
    def is_valid(score_doc):
        """Check if score is still valid (within 30 days)"""
        if not score_doc or 'valid_until' not in score_doc:
            return False
        return datetime.utcnow() < score_doc['valid_until']

    @staticmethod
    def get_all_scores(limit=100, skip=0):
        """Get all scores for admin purposes"""
        return list(scores_collection.find().sort('last_calculated', -1).limit(limit).skip(skip))
from datetime import datetime, timedelta
from models import api_requests_collection
from config import Config

class RateLimitingService:
    @staticmethod
    def check_rate_limit(identifier, limit_type='api_key'):
        """Check if request is within rate limits"""
        window_start = datetime.utcnow() - timedelta(minutes=1)
        
        # Count requests in current window
        request_count = api_requests_collection.count_documents({
            'identifier': identifier,
            'type': limit_type,
            'timestamp': {'$gte': window_start}
        })
        
        # Determine limit based on type
        if limit_type == 'api_key':
            limit = Config.MAX_API_REQUESTS_PER_MINUTE
        else:
            limit = 10  # Default limit for other identifiers
        
        if request_count >= limit:
            return False
        
        # Log the request
        api_requests_collection.insert_one({
            'identifier': identifier,
            'type': limit_type,
            'timestamp': datetime.utcnow(),
            'endpoint': 'unknown'  # Would be set by middleware
        })
        
        return True

    @staticmethod
    def cleanup_old_requests(hours=24):
        """Clean up old API request records"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return api_requests_collection.delete_many({
            'timestamp': {'$lt': cutoff_time}
        })
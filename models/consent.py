from datetime import datetime, timedelta
from models import consents_collection

class Consent:
    @staticmethod
    def create(user_id, lender_id, consent_duration_days=90):
        """Create a consent record"""
        valid_until = datetime.utcnow() + timedelta(days=consent_duration_days)
        
        consent = {
            'user_id': user_id,
            'lender_id': lender_id,
            'consent_given': True,
            'valid_until': valid_until,
            'created_at': datetime.utcnow()
        }
        
        result = consents_collection.insert_one(consent)
        return consent if result.inserted_id else None

    @staticmethod
    def check_valid_consent(user_id, lender_id):
        """Check if valid consent exists"""
        return consents_collection.find_one({
            'user_id': user_id,
            'lender_id': lender_id,
            'consent_given': True,
            'valid_until': {'$gt': datetime.utcnow()}
        })

    @staticmethod
    def get_user_consents(user_id):
        """Get all consents for a user"""
        return list(consents_collection.find({
            'user_id': user_id,
            'consent_given': True
        }).sort('created_at', -1))

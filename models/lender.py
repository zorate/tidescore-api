from datetime import datetime
import secrets
from models import lenders_collection

class Lender:
    @staticmethod
    def create(lender_data):
        """Create a new lender with API key"""
        lender = {
            '_id': f"lender-{secrets.token_hex(8)}",
            'name': lender_data.get('name'),
            'contact_email': lender_data.get('contact_email'),
            'api_key': f"tsk_{secrets.token_hex(32)}",  # TideScore Key
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = lenders_collection.insert_one(lender)
        return lender if result.inserted_id else None

    @staticmethod
    def find_by_api_key(api_key):
        """Find lender by API key"""
        return lenders_collection.find_one({'api_key': api_key, 'is_active': True})

    @staticmethod
    def find_by_id(lender_id):
        """Find lender by ID"""
        return lenders_collection.find_one({'_id': lender_id, 'is_active': True})
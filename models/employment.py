from datetime import datetime
from models import employment_collection

class Employment:
    @staticmethod
    def create_or_update(user_id, employment_data):
        """Create or update employment information"""
        employment = {
            'user_id': user_id,
            'status': employment_data.get('status'),
            'employer_name': employment_data.get('employer_name'),
            'monthly_income': float(employment_data.get('monthly_income', 0)),
            'industry': employment_data.get('industry'),
            'employment_date': employment_data.get('employment_date'),
            'updated_at': datetime.utcnow()
        }
        
        # Upsert employment record
        result = employment_collection.update_one(
            {'user_id': user_id},
            {'$set': employment},
            upsert=True
        )
        
        return employment_collection.find_one({'user_id': user_id})

    @staticmethod
    def find_by_user_id(user_id):
        """Find employment by user ID"""
        return employment_collection.find_one({'user_id': user_id})

    @staticmethod
    def delete_by_user_id(user_id):
        """Delete employment record by user ID"""
        return employment_collection.delete_one({'user_id': user_id})
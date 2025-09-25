from datetime import datetime
from models import guarantors_collection

class Guarantor:
    @staticmethod
    def create(user_id, guarantor_data):
        """Create a new guarantor record"""
        guarantor = {
            'user_id': user_id,
            'name': guarantor_data.get('name'),
            'phone': guarantor_data.get('phone'),
            'email': guarantor_data.get('email'),
            'relationship': guarantor_data.get('relationship'),
            'address': guarantor_data.get('address'),
            'verified': False,
            'created_at': datetime.utcnow()
        }
        
        result = guarantors_collection.insert_one(guarantor)
        return guarantor if result.inserted_id else None

    @staticmethod
    def find_by_user_id(user_id):
        """Find all guarantors for a user"""
        return list(guarantors_collection.find({'user_id': user_id}))

    @staticmethod
    def verify_guarantor(guarantor_id):
        """Mark guarantor as verified"""
        return guarantors_collection.update_one(
            {'_id': guarantor_id},
            {'$set': {'verified': True, 'verified_at': datetime.utcnow()}}
        )
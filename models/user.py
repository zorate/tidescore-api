from datetime import datetime
from models import users_collection
from bson import ObjectId

class User:
    @staticmethod
    def create(user_data):
        """Create a new user"""
        user = {
            '_id': f"user-{ObjectId()}",
            'full_name': user_data.get('full_name'),
            'email': user_data.get('email').lower(),
            'phone': user_data.get('phone'),
            'bvn': user_data.get('bvn'),
            'dob': user_data.get('dob'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True
        }
        
        result = users_collection.insert_one(user)
        return user['_id'] if result.inserted_id else None

    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        return users_collection.find_one({'email': email.lower()})

    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        return users_collection.find_one({'_id': user_id})

    @staticmethod
    def update(user_id, update_data):
        """Update user information"""
        update_data['updated_at'] = datetime.utcnow()
        return users_collection.update_one(
            {'_id': user_id},
            {'$set': update_data}
        )
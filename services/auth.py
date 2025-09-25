import jwt
import bcrypt
from datetime import datetime, timedelta
from config import Config

class AuthService:
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed_password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def generate_user_token(user_id, email):
        """Generate JWT token for users"""
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES,
            'iat': datetime.utcnow(),
            'type': 'user'
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def verify_user_token(token):
        """Verify JWT token for users"""
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != 'user':
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def verify_lender_api_key(api_key):
        """Verify lender API key"""
        from models.lender import Lender
        return Lender.find_by_api_key(api_key)

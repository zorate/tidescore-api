from flask import request, jsonify
from services.auth import AuthService
from services.rate_limiting import RateLimitingService

def lender_auth_required(f):
    """Decorator for lender API key authentication"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        lender = AuthService.verify_lender_api_key(api_key)
        if not lender:
            return jsonify({'error': 'Invalid API key'}), 401
        
        # Check rate limiting
        if not RateLimitingService.check_rate_limit(api_key, 'api_key'):
            return jsonify({'error': 'Rate limit exceeded'}), 429
        
        # Add lender to request context
        request.lender = lender
        return f(*args, **kwargs)
    
    return decorated_function

def user_auth_required(f):
    """Decorator for user JWT authentication"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization header required'}), 401
        
        token = auth_header.split(' ')[1]
        user_data = AuthService.verify_user_token(token)
        
        if not user_data:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Check rate limiting
        if not RateLimitingService.check_rate_limit(user_data['user_id'], 'user'):
            return jsonify({'error': 'Rate limit exceeded'}), 429
        
        # Add user data to request context
        request.user_data = user_data
        return f(*args, **kwargs)
    
    return decorated_function

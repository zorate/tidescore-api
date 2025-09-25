from flask import Blueprint, request, jsonify
from models.user import User
from models.score import Score
from models.lender import Lender

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/v1/admin/users', methods=['GET'])
def get_all_users():
    """Admin endpoint to get all users"""
    # Add admin authentication here (simplified for example)
    admin_key = request.headers.get('X-Admin-Key')
    if admin_key != 'your-admin-secret-key':  # In production, use proper admin auth
        return jsonify({'error': 'Admin access required'}), 401
    
    limit = int(request.args.get('limit', 100))
    skip = int(request.args.get('skip', 0))
    
    users = list(User.users_collection.find().limit(limit).skip(skip))
    
    # Remove sensitive data
    for user in users:
        user.pop('bvn', None)
        user.pop('_id', None)
    
    return jsonify({'users': users, 'total': len(users)}), 200

@admin_bp.route('/api/v1/admin/scores', methods=['GET'])
def get_all_scores():
    """Admin endpoint to get all scores"""
    admin_key = request.headers.get('X-Admin-Key')
    if admin_key != 'your-admin-secret-key':
        return jsonify({'error': 'Admin access required'}), 401
    
    limit = int(request.args.get('limit', 100))
    skip = int(request.args.get('skip', 0))
    
    scores = Score.get_all_scores(limit, skip)
    
    # Format scores for response
    formatted_scores = []
    for score in scores:
        formatted_scores.append({
            'user_id': score['user_id'],
            'score': score['score'],
            'status': score['status'],
            'last_calculated': score['last_calculated'].isoformat() + 'Z',
            'valid_until': score['valid_until'].isoformat() + 'Z',
            'data_points_used': score.get('data_points_used', 0)
        })
    
    return jsonify({'scores': formatted_scores, 'total': len(formatted_scores)}), 200

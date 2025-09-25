from flask import Blueprint, request, jsonify
from services.auth import AuthService
from services.scoring import ScoringService
from models.score import Score
from models.consent import Consent
from models.user import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/v1/users/score/check', methods=['POST'])
def check_score():
    """Borrower self-check endpoint"""
    # Authenticate user via JWT
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization header required'}), 401
    
    token = auth_header.split(' ')[1]
    user_data = AuthService.verify_user_token(token)
    
    if not user_data:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    user_id = user_data['user_id']
    
    # Calculate score
    score_data = ScoringService.calculate_score(user_id)
    
    # Store the score
    stored_score = Score.create_or_update(user_id, score_data)
    
    response = {
        'user_id': user_id,
        'score': score_data['score'],
        'status': score_data['status'],
        'last_calculated': stored_score['last_calculated'].isoformat() + 'Z',
        'valid_until': stored_score['valid_until'].isoformat() + 'Z',
        'source': 'calculated',
        'advice': score_data['advice'],
        'breakdown': score_data.get('breakdown', {}),
        'data_points_used': score_data.get('data_points_used', 0)
    }
    
    return jsonify(response), 200

@users_bp.route('/api/v1/users/<user_id>/authorize', methods=['POST'])
def authorize_lender(user_id):
    """Borrower authorizes score sharing with lender"""
    # Authenticate user via JWT
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization header required'}), 401
    
    token = auth_header.split(' ')[1]
    user_data = AuthService.verify_user_token(token)
    
    if not user_data or user_data['user_id'] != user_id:
        return jsonify({'error': 'Invalid token or user ID mismatch'}), 401
    
    lender_id = request.json.get('lender_id')
    if not lender_id:
        return jsonify({'error': 'Lender ID required'}), 400
    
    # Create consent
    consent = Consent.create(user_id, lender_id)
    
    if not consent:
        return jsonify({'error': 'Failed to create consent'}), 500
    
    return jsonify({
        'user_id': user_id,
        'lender_id': lender_id,
        'consent_given': True,
        'valid_until': consent['valid_until'].isoformat() + 'Z',
        'message': 'Lender authorized to access your score'
    }), 201
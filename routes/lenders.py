from flask import Blueprint, request, jsonify
from services.auth import AuthService
from services.cache import CacheService
from models.consent import Consent
from models.user import User

lenders_bp = Blueprint('lenders', __name__)

@lenders_bp.route('/api/v1/lenders/<lender_id>/borrowers/<borrower_id>/score', methods=['GET'])
def get_borrower_score(lender_id, borrower_id):
    # Authenticate lender via API key
    api_key = request.headers.get('X-API-Key')
    lender = AuthService.verify_lender_api_key(api_key)
    
    if not lender or lender['_id'] != lender_id:
        return jsonify({'error': 'Invalid API key or lender ID'}), 401
    
    # Check if borrower exists
    borrower = User.find_by_id(borrower_id)
    if not borrower:
        return jsonify({'error': 'Borrower not found'}), 404
    
    # Check consent
    consent = Consent.check_valid_consent(borrower_id, lender_id)
    if not consent:
        return jsonify({
            'error': 'Borrower consent required',
            'code': 'CONSENT_REQUIRED',
            'message': 'Borrower must provide consent before score can be accessed'
        }), 403
    
    # Check if refresh is requested
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    # Get score from cache or recalculate
    cached_score, source = CacheService.get_cached_score(borrower_id, force_refresh)
    
    if source == 'recalculate':
        # Recalculate score
        score_data = CacheService.refresh_score(borrower_id)
        source = 'recalculated'
    else:
        score_data = cached_score
        source = 'cached'
    
    if not score_data or score_data.get('score') is None:
        return jsonify({
            'borrower_id': borrower_id,
            'score': None,
            'status': 'Unavailable',
            'reason': 'Insufficient data. Borrower must submit financial information.',
            'code': 'INSUFFICIENT_DATA'
        }), 200
    
    # Format response
    response = {
        'borrower_id': borrower_id,
        'score': score_data['score'],
        'status': score_data['status'],
        'last_calculated': score_data['last_calculated'].isoformat() + 'Z',
        'valid_until': score_data['valid_until'].isoformat() + 'Z',
        'source': source,
        'advice': score_data['advice'],
        'breakdown': score_data.get('breakdown', {})
    }
    
    return jsonify(response), 200
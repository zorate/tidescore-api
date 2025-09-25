from flask import Blueprint, request, jsonify
from middleware.auth_middleware import user_auth_required
from models.transactions import Transaction
from models.employment import Employment
from models.guarantors import Guarantor

data_bp = Blueprint('data', __name__)

@data_bp.route('/api/v1/users/data/transactions', methods=['POST'])
@user_auth_required
def submit_transactions():
    """Submit transaction data for scoring"""
    user_id = request.user_data['user_id']
    transactions_data = request.json.get('transactions', [])
    
    if not transactions_data:
        return jsonify({'error': 'No transactions provided'}), 400
    
    try:
        count = Transaction.bulk_create(user_id, transactions_data)
        return jsonify({
            'message': f'Successfully submitted {count} transactions',
            'user_id': user_id,
            'transactions_added': count
        }), 201
    except Exception as e:
        return jsonify({'error': f'Failed to submit transactions: {str(e)}'}), 500

@data_bp.route('/api/v1/users/data/employment', methods=['POST'])
@user_auth_required
def submit_employment():
    """Submit employment information"""
    user_id = request.user_data['user_id']
    employment_data = request.json
    
    if not employment_data.get('status'):
        return jsonify({'error': 'Employment status required'}), 400
    
    try:
        employment = Employment.create_or_update(user_id, employment_data)
        return jsonify({
            'message': 'Employment information updated',
            'user_id': user_id,
            'employment_status': employment['status']
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to update employment: {str(e)}'}), 500

@data_bp.route('/api/v1/users/data/guarantors', methods=['POST'])
@user_auth_required
def submit_guarantor():
    """Submit guarantor information"""
    user_id = request.user_data['user_id']
    guarantor_data = request.json
    
    if not guarantor_data.get('name') or not guarantor_data.get('phone'):
        return jsonify({'error': 'Guarantor name and phone required'}), 400
    
    try:
        guarantor = Guarantor.create(user_id, guarantor_data)
        return jsonify({
            'message': 'Guarantor information added',
            'user_id': user_id,
            'guarantor_id': guarantor['_id']
        }), 201
    except Exception as e:
        return jsonify({'error': f'Failed to add guarantor: {str(e)}'}), 500
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.lenders import lenders_bp
from routes.users import users_bp
from routes.admin import admin_bp
from routes.data_submission import data_bp

# Create app instance directly (not inside a function)
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Register blueprints
app.register_blueprint(lenders_bp)
app.register_blueprint(users_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(data_bp)

# Root endpoint
@app.route('/')
def home():
    return jsonify({
        'message': 'TideScore API is running!',
        'version': '1.0.0',
        'status': 'operational'
    })

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'TideScore API'})

# API documentation endpoint
@app.route('/api/v1/docs', methods=['GET'])
def api_docs():
    return jsonify({
        'message': 'TideScore API Documentation',
        'endpoints': {
            'lenders': {
                'GET /api/v1/lenders/{lender_id}/borrowers/{borrower_id}/score': 'Get borrower score'
            },
            'users': {
                'POST /api/v1/users/score/check': 'Check own score',
                'POST /api/v1/users/{user_id}/authorize': 'Authorize lender'
            }
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Make sure app variable is available for Gunicorn
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

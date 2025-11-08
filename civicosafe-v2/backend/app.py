from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize database on startup
from database.db import init_database
try:
    init_database()
    print('✅ Database initialized')
except Exception as e:
    print(f'⚠️ Database initialization warning: {e}')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'your-secret-key-change-this-in-production')

# Handle OPTIONS preflight requests globally - BEFORE CORS and authentication
@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        response = jsonify({'success': True})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5500')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Max-Age', '3600')
        return response

# CORS configuration - allow OPTIONS preflight requests
CORS(app, 
     origins=[os.getenv('FRONTEND_URL', 'http://localhost:5500')], 
     supports_credentials=True,
     allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# Import blueprints
from routes.auth import auth_bp
from routes.incidents import incidents_bp
from routes.alerts import alerts_bp
from routes.members import members_bp
from routes.dashboard import dashboard_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(incidents_bp, url_prefix='/api/incidents')
app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
app.register_blueprint(members_bp, url_prefix='/api/members')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

# Root route
@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'Civicosafe API is running',
        'endpoints': {
            'health': '/api/health',
            'auth': '/api/auth',
            'incidents': '/api/incidents',
            'alerts': '/api/alerts',
            'members': '/api/members',
            'dashboard': '/api/dashboard'
        }
    })

# Favicon route (prevents 404 errors in browser console)
@app.route('/favicon.ico')
def favicon():
    from flask import Response
    return Response(status=204)  # No Content

# Health check
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'Civicosafe API is running'
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Route not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal Server Error'
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    print(f'🚀 Server running on http://localhost:{port}')
    print(f'📡 API endpoint: http://localhost:{port}/api')
    app.run(host='0.0.0.0', port=port, debug=True)


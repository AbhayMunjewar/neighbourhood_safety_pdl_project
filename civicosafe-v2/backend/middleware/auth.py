from functools import wraps
from flask import request, jsonify
import jwt
import os
from database.db import get

JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-this-in-production')

def authenticate_token(f):
    """Decorator to authenticate JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Handle OPTIONS preflight requests - should be caught by global handler, but double-check
        if request.method == 'OPTIONS':
            response = jsonify({'success': True})
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5500')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
        
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer TOKEN
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid token format'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Access token required'
            }), 401
        
        try:
            # Decode token
            decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            
            # Get user from database
            user = get('SELECT id, email, name, role FROM users WHERE id = ?', (decoded['userId'],))
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'User not found'
                }), 401
            
            # Add user to request context
            request.user = user
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token has expired'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated


from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import os
from database.db import get, run

auth_bp = Blueprint('auth', __name__)
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-this-in-production')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('name') or not data.get('name').strip():
            return jsonify({
                'success': False,
                'message': 'Name is required'
            }), 400
        
        if not data.get('email') or '@' not in data.get('email', ''):
            return jsonify({
                'success': False,
                'message': 'Valid email is required'
            }), 400
        
        if not data.get('password') or len(data.get('password', '')) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters'
            }), 400
        
        name = data['name'].strip()
        email = data['email']
        password = data['password']
        
        # Check if user exists
        existing_user = get('SELECT id FROM users WHERE email = ?', (email,))
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 400
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user
        result = run(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed_password)
        )
        
        # Also create member record
        run(
            'INSERT INTO members (user_id, role) VALUES (?, ?)',
            (result['id'], 'member')
        )
        
        # Generate token
        token = jwt.encode(
            {'userId': result['id'], 'email': email},
            JWT_SECRET,
            algorithm='HS256'
        )
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': result['id'],
                'name': name,
                'email': email
            }
        }), 201
        
    except Exception as e:
        print(f'Registration error: {e}')
        return jsonify({
            'success': False,
            'message': 'Server error during registration'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('email') or '@' not in data.get('email', ''):
            return jsonify({
                'success': False,
                'message': 'Valid email is required'
            }), 400
        
        if not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Password is required'
            }), 400
        
        email = data['email']
        password = data['password']
        
        # Find user
        user = get('SELECT * FROM users WHERE email = ?', (email,))
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Generate token
        token = jwt.encode(
            {'userId': user['id'], 'email': user['email']},
            JWT_SECRET,
            algorithm='HS256'
        )
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
        })
        
    except Exception as e:
        print(f'Login error: {e}')
        return jsonify({
            'success': False,
            'message': 'Server error during login'
        }), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                'success': False,
                'message': 'No token provided'
            }), 401
        
        token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
        
        # Decode token
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = get('SELECT id, name, email, role, verified FROM users WHERE id = ?', (decoded['userId'],))
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': dict(user)
        })
        
    except jwt.ExpiredSignatureError:
        return jsonify({
            'success': False,
            'message': 'Token has expired'
        }), 401
    except jwt.InvalidTokenError:
        return jsonify({
            'success': False,
            'message': 'Invalid token'
        }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error retrieving user'
        }), 500


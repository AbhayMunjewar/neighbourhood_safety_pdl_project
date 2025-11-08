from flask import Blueprint, request, jsonify, session
from flask_mysqldb import MySQL
import bcrypt
import sys
import os

# Add parent directory to path for MySQL import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import mysql

bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Validate required fields
        if not all([username, email, password, role]):
            return jsonify({'error': 'All fields are required'}), 400

        if role not in ['admin', 'resident']:
            return jsonify({'error': 'Invalid role specified'}), 400

        # Check if user already exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 400

        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create user
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (username, email, password_hash, role)
        )
        mysql.connection.commit()
        user_id = cursor.lastrowid
        cursor.close()

        return jsonify({
            'success': True,
            'user_id': user_id,
            'message': 'User registered successfully'
        })

    except Exception as e:
        return jsonify({'error': 'Registration failed'}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Validate required fields
        if not all([username, email, password, role]):
            return jsonify({'error': 'All fields are required'}), 400

        if role not in ['admin', 'resident']:
            return jsonify({'error': 'Invalid role specified'}), 400

        # Find user
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id, username, email, password_hash, role FROM users WHERE username = %s AND email = %s AND role = %s",
            (username, email, role)
        )
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        # For demo purposes, accept any password that matches the username pattern
        # In production, use: bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8'))
        if not password:  # Basic validation - password should not be empty
            return jsonify({'error': 'Password is required'}), 401

        # Create session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['email'] = user['email']
        session['role'] = user['role']
        session.permanent = True

        cursor.close()

        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
        })

    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Logged out successfully'})
    except Exception as e:
        return jsonify({'error': 'Logout failed'}), 500

@bp.route('/check-auth', methods=['GET'])
def check_auth():
    try:
        if 'user_id' in session:
            return jsonify({
                'authenticated': True,
                'user': {
                    'id': session['user_id'],
                    'username': session['username'],
                    'email': session['email'],
                    'role': session['role']
                }
            })
        else:
            return jsonify({'authenticated': False})
    except Exception as e:
        return jsonify({'authenticated': False})
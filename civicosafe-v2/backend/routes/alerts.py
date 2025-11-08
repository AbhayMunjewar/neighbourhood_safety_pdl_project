from flask import Blueprint, request, jsonify
from middleware.auth import authenticate_token
from database.db import get, run, query

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/', methods=['GET'])
@authenticate_token
def get_alerts():
    try:
        # Get query parameters
        alert_type = request.args.get('type')
        status = request.args.get('status')
        
        # Build query
        sql = '''
            SELECT a.*, u.name as author_name
            FROM alerts a
            JOIN users u ON a.user_id = u.id
            WHERE 1=1
        '''
        params = []
        
        if alert_type:
            sql += ' AND a.type = ?'
            params.append(alert_type)
        
        if status:
            sql += ' AND a.status = ?'
            params.append(status)
        
        sql += ' ORDER BY a.created_at DESC'
        
        alerts = query(sql, tuple(params))
        
        return jsonify({
            'success': True,
            'data': alerts
        })
    except Exception as e:
        print(f'Error fetching alerts: {e}')
        return jsonify({
            'success': False,
            'message': 'Error fetching alerts'
        }), 500

@alerts_bp.route('/', methods=['POST'])
@authenticate_token
def create_alert():
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('title') or not data.get('title').strip():
            return jsonify({
                'success': False,
                'message': 'Title is required'
            }), 400
        
        if not data.get('message') or not data.get('message').strip():
            return jsonify({
                'success': False,
                'message': 'Message is required'
            }), 400
        
        alert_data = {
            'user_id': request.user['id'],
            'title': data['title'].strip(),
            'message': data['message'].strip(),
            'type': data.get('type', 'general'),
            'priority': data.get('priority', 'medium')
        }
        
        result = run('''
            INSERT INTO alerts (user_id, title, message, type, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            alert_data['user_id'],
            alert_data['title'],
            alert_data['message'],
            alert_data['type'],
            alert_data['priority']
        ))
        
        alert = get('SELECT * FROM alerts WHERE id = ?', (result['id'],))
        
        return jsonify({
            'success': True,
            'message': 'Alert created successfully',
            'data': alert
        }), 201
        
    except Exception as e:
        print(f'Error creating alert: {e}')
        return jsonify({
            'success': False,
            'message': 'Error creating alert'
        }), 500


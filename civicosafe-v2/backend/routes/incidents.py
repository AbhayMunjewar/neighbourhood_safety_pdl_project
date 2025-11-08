from flask import Blueprint, request, jsonify
from middleware.auth import authenticate_token
from database.db import get, run, query

incidents_bp = Blueprint('incidents', __name__)

@incidents_bp.route('/', methods=['GET'])
@authenticate_token
def get_incidents():
    try:
        incidents = query('''
            SELECT i.*, u.name as reporter_name, u.email as reporter_email
            FROM incidents i
            JOIN users u ON i.user_id = u.id
            ORDER BY i.created_at DESC
        ''')
        
        return jsonify({
            'success': True,
            'data': incidents
        })
    except Exception as e:
        print(f'Error fetching incidents: {e}')
        return jsonify({
            'success': False,
            'message': 'Error fetching incidents'
        }), 500

@incidents_bp.route('/<int:incident_id>', methods=['GET'])
@authenticate_token
def get_incident(incident_id):
    try:
        incident = get('''
            SELECT i.*, u.name as reporter_name, u.email as reporter_email
            FROM incidents i
            JOIN users u ON i.user_id = u.id
            WHERE i.id = ?
        ''', (incident_id,))
        
        if not incident:
            return jsonify({
                'success': False,
                'message': 'Incident not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': incident
        })
    except Exception as e:
        print(f'Error fetching incident: {e}')
        return jsonify({
            'success': False,
            'message': 'Error fetching incident'
        }), 500

@incidents_bp.route('/', methods=['POST'])
@authenticate_token
def create_incident():
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['type', 'location', 'date', 'time', 'severity']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'{field.capitalize()} is required'
                }), 400
        
        incident_data = {
            'user_id': request.user['id'],
            'type': data['type'],
            'location': data['location'],
            'date': data['date'],
            'time': data['time'],
            'severity': data['severity'],
            'description': data.get('description', '')
        }
        
        result = run('''
            INSERT INTO incidents (user_id, type, location, date, time, severity, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            incident_data['user_id'],
            incident_data['type'],
            incident_data['location'],
            incident_data['date'],
            incident_data['time'],
            incident_data['severity'],
            incident_data['description']
        ))
        
        if not result or not result.get('id'):
            raise Exception('Failed to create incident - no ID returned')
        
        incident = get('SELECT * FROM incidents WHERE id = ?', (result['id'],))
        
        if not incident:
            raise Exception(f'Failed to retrieve created incident with id {result["id"]}')
        
        return jsonify({
            'success': True,
            'message': 'Incident reported successfully',
            'data': incident
        }), 201
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f'Error creating incident: {e}')
        print(f'Traceback: {error_trace}')
        return jsonify({
            'success': False,
            'message': f'Error creating incident: {str(e)}'
        }), 500

@incidents_bp.route('/<int:incident_id>/status', methods=['PATCH'])
@authenticate_token
def update_incident_status(incident_id):
    try:
        data = request.get_json()
        status = data.get('status')
        
        # Validation
        valid_statuses = ['pending', 'investigating', 'resolved', 'closed']
        if status not in valid_statuses:
            return jsonify({
                'success': False,
                'message': 'Invalid status'
            }), 400
        
        run('UPDATE incidents SET status = ? WHERE id = ?', (status, incident_id))
        
        return jsonify({
            'success': True,
            'message': 'Incident status updated'
        })
        
    except Exception as e:
        print(f'Error updating incident: {e}')
        return jsonify({
            'success': False,
            'message': 'Error updating incident'
        }), 500


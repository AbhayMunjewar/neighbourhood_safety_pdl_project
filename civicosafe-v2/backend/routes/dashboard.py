from flask import Blueprint, jsonify
from middleware.auth import authenticate_token
from database.db import get, query

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@authenticate_token
def get_stats():
    try:
        # Total members
        total_members_result = get('SELECT COUNT(*) as count FROM users')
        total_members = total_members_result['count'] if total_members_result else 0
        
        # Total incidents
        total_incidents_result = get('SELECT COUNT(*) as count FROM incidents')
        total_incidents = total_incidents_result['count'] if total_incidents_result else 0
        
        # Active alerts
        active_alerts_result = get('SELECT COUNT(*) as count FROM alerts WHERE status = ?', ('active',))
        active_alerts = active_alerts_result['count'] if active_alerts_result else 0
        
        # Recent incidents (last 7 days)
        recent_incidents_result = get('''
            SELECT COUNT(*) as count 
            FROM incidents 
            WHERE date(created_at) >= date('now', '-7 days')
        ''')
        recent_incidents = recent_incidents_result['count'] if recent_incidents_result else 0
        
        # Incidents by type
        incidents_by_type = query('''
            SELECT type, COUNT(*) as count
            FROM incidents
            GROUP BY type
        ''')
        
        # Incidents by status
        incidents_by_status = query('''
            SELECT status, COUNT(*) as count
            FROM incidents
            GROUP BY status
        ''')
        
        return jsonify({
            'success': True,
            'data': {
                'totalMembers': total_members,
                'totalIncidents': total_incidents,
                'activeAlerts': active_alerts,
                'recentIncidents': recent_incidents,
                'incidentsByType': incidents_by_type,
                'incidentsByStatus': incidents_by_status
            }
        })
    except Exception as e:
        print(f'Error fetching dashboard stats: {e}')
        return jsonify({
            'success': False,
            'message': 'Error fetching dashboard statistics'
        }), 500

@dashboard_bp.route('/activity', methods=['GET'])
@authenticate_token
def get_activity():
    try:
        activities = query('''
            SELECT 
                'incident' as type,
                i.type as title,
                i.location as description,
                i.created_at as timestamp,
                u.name as user_name
            FROM incidents i
            JOIN users u ON i.user_id = u.id
            UNION ALL
            SELECT 
                'alert' as type,
                a.title,
                a.message as description,
                a.created_at as timestamp,
                u.name as user_name
            FROM alerts a
            JOIN users u ON a.user_id = u.id
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        
        return jsonify({
            'success': True,
            'data': activities
        })
    except Exception as e:
        print(f'Error fetching activity: {e}')
        return jsonify({
            'success': False,
            'message': 'Error fetching activity'
        }), 500


from flask import Blueprint, request, jsonify, session
from flask_mysqldb import MySQL
import sys
import os

# Add parent directory to path for MySQL import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import mysql

bp = Blueprint('dashboard', __name__, url_prefix='/api/stats')

def require_auth():
    if 'user_id' not in session:
        return False
    return True

@bp.route('/dashboard', methods=['GET'])
def get_dashboard_stats():
    try:
        if not require_auth():
            return jsonify({'error': 'Authentication required'}), 401

        cursor = mysql.connection.cursor()

        # Get total incidents count
        cursor.execute("SELECT COUNT(*) as total FROM incidents")
        total_incidents = cursor.fetchone()['total']

        # Get incidents by status
        cursor.execute("SELECT status, COUNT(*) as count FROM incidents GROUP BY status")
        status_counts = cursor.fetchall()

        open_cases = 0
        investigating = 0
        resolved = 0

        for row in status_counts:
            if row['status'] == 'open':
                open_cases = row['count']
            elif row['status'] == 'investigating':
                investigating = row['count']
            elif row['status'] == 'resolved':
                resolved = row['count']

        # Get recent incidents (last 5)
        cursor.execute(
            """SELECT i.*, u.username FROM incidents i
               JOIN users u ON i.user_id = u.id
               ORDER BY i.created_at DESC LIMIT 5"""
        )
        recent_incidents = cursor.fetchall()

        # Get incidents by priority
        cursor.execute("SELECT priority, COUNT(*) as count FROM incidents GROUP BY priority")
        priority_counts = cursor.fetchall()

        # Get incidents by type
        cursor.execute("SELECT incident_type, COUNT(*) as count FROM incidents GROUP BY incident_type")
        type_counts = cursor.fetchall()

        cursor.close()

        return jsonify({
            'total_incidents': total_incidents,
            'open_cases': open_cases,
            'investigating': investigating,
            'resolved': resolved,
            'recent_incidents': recent_incidents,
            'priority_breakdown': priority_counts,
            'type_breakdown': type_counts
        })

    except Exception as e:
        return jsonify({'error': 'Failed to fetch dashboard statistics'}), 500

@bp.route('/user-activity', methods=['GET'])
def get_user_activity():
    try:
        if not require_auth():
            return jsonify({'error': 'Authentication required'}), 401

        cursor = mysql.connection.cursor()

        # Get user's incident statistics
        cursor.execute(
            "SELECT COUNT(*) as total FROM incidents WHERE user_id = %s",
            (session['user_id'],)
        )
        user_total = cursor.fetchone()['total']

        # Get user's incidents by status
        cursor.execute(
            """SELECT status, COUNT(*) as count FROM incidents
               WHERE user_id = %s GROUP BY status""",
            (session['user_id'],)
        )
        user_status_counts = cursor.fetchall()

        user_open = 0
        user_investigating = 0
        user_resolved = 0

        for row in user_status_counts:
            if row['status'] == 'open':
                user_open = row['count']
            elif row['status'] == 'investigating':
                user_investigating = row['count']
            elif row['status'] == 'resolved':
                user_resolved = row['count']

        # Get user's recent incidents
        cursor.execute(
            """SELECT * FROM incidents
               WHERE user_id = %s
               ORDER BY created_at DESC LIMIT 5""",
            (session['user_id'],)
        )
        user_recent = cursor.fetchall()

        cursor.close()

        return jsonify({
            'user_total_incidents': user_total,
            'user_open_cases': user_open,
            'user_investigating': user_investigating,
            'user_resolved': user_resolved,
            'user_recent_incidents': user_recent
        })

    except Exception as e:
        return jsonify({'error': 'Failed to fetch user activity'}), 500
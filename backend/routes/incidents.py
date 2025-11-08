from flask import Blueprint, request, jsonify, session
from flask_mysqldb import MySQL
import sys
import os

# Add parent directory to path for MySQL import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import mysql

bp = Blueprint('incidents', __name__, url_prefix='/api/incidents')

def require_auth():
    if 'user_id' not in session:
        return False
    return True

@bp.route('/', methods=['GET'])
def get_incidents():
    try:
        # Get query parameters for filtering and sorting
        status_filter = request.args.get('status', '')
        priority_filter = request.args.get('priority', '')
        search = request.args.get('search', '')
        sort_by = request.args.get('sort', 'created_at')
        order = request.args.get('order', 'DESC')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Build query
        query = "SELECT i.*, u.username, u.role FROM incidents i JOIN users u ON i.user_id = u.id WHERE 1=1"
        params = []

        if status_filter:
            query += " AND i.status = %s"
            params.append(status_filter)

        if priority_filter:
            query += " AND i.priority = %s"
            params.append(priority_filter)

        if search:
            query += " AND (i.title LIKE %s OR i.location LIKE %s OR i.description LIKE %s)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term, search_term])

        # Add sorting
        valid_sort_fields = ['created_at', 'priority', 'status', 'title', 'location']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'

        valid_orders = ['ASC', 'DESC']
        if order not in valid_orders:
            order = 'DESC'

        query += f" ORDER BY i.{sort_by} {order}"

        # Add pagination
        offset = (page - 1) * per_page
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        cursor = mysql.connection.cursor()
        cursor.execute(query, params)
        incidents = cursor.fetchall()

        # Get total count for pagination
        count_query = "SELECT COUNT(*) as total FROM incidents i WHERE 1=1"
        count_params = []

        if status_filter:
            count_query += " AND i.status = %s"
            count_params.append(status_filter)

        if priority_filter:
            count_query += " AND i.priority = %s"
            count_params.append(priority_filter)

        if search:
            count_query += " AND (i.title LIKE %s OR i.location LIKE %s OR i.description LIKE %s)"
            search_term = f"%{search}%"
            count_params.extend([search_term, search_term, search_term])

        cursor.execute(count_query, count_params)
        total_count = cursor.fetchone()['total']
        cursor.close()

        return jsonify({
            'incidents': incidents,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_count,
                'pages': (total_count + per_page - 1) // per_page
            }
        })

    except Exception as e:
        return jsonify({'error': 'Failed to fetch incidents'}), 500

@bp.route('/', methods=['POST'])
def create_incident():
    try:
        if not require_auth():
            return jsonify({'error': 'Authentication required'}), 401

        data = request.get_json()
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        location = data.get('location', '').strip()
        incident_type = data.get('incident_type', '').strip()
        priority = data.get('priority', 'medium')

        # Validate required fields
        if not all([title, description, location, incident_type]):
            return jsonify({'error': 'All fields are required'}), 400

        if priority not in ['low', 'medium', 'high']:
            priority = 'medium'

        # Validate incident type
        valid_types = ['Theft', 'Vandalism', 'Safety Issue', 'Noise', 'Other']
        if incident_type not in valid_types:
            incident_type = 'Other'

        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO incidents (user_id, title, description, location, incident_type, priority, status)
               VALUES (%s, %s, %s, %s, %s, %s, 'open')""",
            (session['user_id'], title, description, location, incident_type, priority)
        )
        mysql.connection.commit()
        incident_id = cursor.lastrowid
        cursor.close()

        return jsonify({
            'success': True,
            'incident_id': incident_id,
            'message': 'Incident created successfully'
        })

    except Exception as e:
        return jsonify({'error': 'Failed to create incident'}), 500

@bp.route('/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT i.*, u.username, u.role FROM incidents i
               JOIN users u ON i.user_id = u.id WHERE i.id = %s""",
            (incident_id,)
        )
        incident = cursor.fetchone()
        cursor.close()

        if not incident:
            return jsonify({'error': 'Incident not found'}), 404

        return jsonify({'incident': incident})

    except Exception as e:
        return jsonify({'error': 'Failed to fetch incident'}), 500

@bp.route('/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    try:
        if not require_auth():
            return jsonify({'error': 'Authentication required'}), 401

        data = request.get_json()
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        location = data.get('location', '').strip()
        incident_type = data.get('incident_type', '').strip()
        priority = data.get('priority', 'medium')
        status = data.get('status', 'open')

        # Check if incident exists and user has permission
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT user_id FROM incidents WHERE id = %s", (incident_id,))
        incident = cursor.fetchone()

        if not incident:
            cursor.close()
            return jsonify({'error': 'Incident not found'}), 404

        # Check if user is the owner or admin
        if incident['user_id'] != session['user_id'] and session['role'] != 'admin':
            cursor.close()
            return jsonify({'error': 'Permission denied'}), 403

        # Validate inputs
        if priority not in ['low', 'medium', 'high']:
            priority = 'medium'

        if status not in ['open', 'investigating', 'resolved']:
            status = 'open'

        valid_types = ['Theft', 'Vandalism', 'Safety Issue', 'Noise', 'Other']
        if incident_type and incident_type not in valid_types:
            incident_type = 'Other'

        # Update incident
        update_fields = []
        params = []

        if title:
            update_fields.append("title = %s")
            params.append(title)

        if description:
            update_fields.append("description = %s")
            params.append(description)

        if location:
            update_fields.append("location = %s")
            params.append(location)

        if incident_type:
            update_fields.append("incident_type = %s")
            params.append(incident_type)

        update_fields.append("priority = %s")
        params.append(priority)

        update_fields.append("status = %s")
        params.append(status)

        params.append(incident_id)

        cursor.execute(
            f"UPDATE incidents SET {', '.join(update_fields)} WHERE id = %s",
            params
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'success': True,
            'message': 'Incident updated successfully'
        })

    except Exception as e:
        return jsonify({'error': 'Failed to update incident'}), 500

@bp.route('/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    try:
        if not require_auth():
            return jsonify({'error': 'Authentication required'}), 401

        # Check if incident exists and user has permission
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT user_id FROM incidents WHERE id = %s", (incident_id,))
        incident = cursor.fetchone()

        if not incident:
            cursor.close()
            return jsonify({'error': 'Incident not found'}), 404

        # Check if user is the owner or admin
        if incident['user_id'] != session['user_id'] and session['role'] != 'admin':
            cursor.close()
            return jsonify({'error': 'Permission denied'}), 403

        # Delete incident
        cursor.execute("DELETE FROM incidents WHERE id = %s", (incident_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'success': True,
            'message': 'Incident deleted successfully'
        })

    except Exception as e:
        return jsonify({'error': 'Failed to delete incident'}), 500
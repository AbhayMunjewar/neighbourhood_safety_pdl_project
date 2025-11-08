from flask import Blueprint, request, jsonify
from middleware.auth import authenticate_token
from database.db import get, run, query

members_bp = Blueprint('members', __name__)

@members_bp.route('/', methods=['GET'])
@authenticate_token
def get_members():
    try:
        search = request.args.get('search', '')
        
        sql = '''
            SELECT u.id, u.name, u.email, u.role, u.verified, m.phone, m.address, m.block_captain
            FROM users u
            LEFT JOIN members m ON u.id = m.user_id
            WHERE 1=1
        '''
        params = []
        
        if search:
            sql += ' AND (u.name LIKE ? OR u.email LIKE ?)'
            search_term = f'%{search}%'
            params.extend([search_term, search_term])
        
        sql += ' ORDER BY u.name ASC'
        
        members = query(sql, tuple(params))
        
        return jsonify({
            'success': True,
            'data': members
        })
    except Exception as e:
        print(f'Error fetching members: {e}')
        return jsonify({
            'success': False,
            'message': 'Error fetching members'
        }), 500

@members_bp.route('/<int:member_id>', methods=['GET'])
@authenticate_token
def get_member(member_id):
    try:
        member = get('''
            SELECT u.id, u.name, u.email, u.role, u.verified, m.phone, m.address, m.block_captain
            FROM users u
            LEFT JOIN members m ON u.id = m.user_id
            WHERE u.id = ?
        ''', (member_id,))
        
        if not member:
            return jsonify({
                'success': False,
                'message': 'Member not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': member
        })
    except Exception as e:
        print(f'Error fetching member: {e}')
        return jsonify({
            'success': False,
            'message': 'Error fetching member'
        }), 500

@members_bp.route('/<int:member_id>', methods=['PATCH'])
@authenticate_token
def update_member(member_id):
    try:
        data = request.get_json()
        
        phone = data.get('phone')
        address = data.get('address')
        block_captain = data.get('block_captain', False)
        
        # Check if member record exists
        existing = get('SELECT id FROM members WHERE user_id = ?', (member_id,))
        
        if existing:
            run('''
                UPDATE members 
                SET phone = ?, address = ?, block_captain = ?
                WHERE user_id = ?
            ''', (phone, address, 1 if block_captain else 0, member_id))
        else:
            run('''
                INSERT INTO members (user_id, phone, address, block_captain)
                VALUES (?, ?, ?, ?)
            ''', (member_id, phone, address, 1 if block_captain else 0))
        
        return jsonify({
            'success': True,
            'message': 'Member profile updated'
        })
        
    except Exception as e:
        print(f'Error updating member: {e}')
        return jsonify({
            'success': False,
            'message': 'Error updating member'
        }), 500


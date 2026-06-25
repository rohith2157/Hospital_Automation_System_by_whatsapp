from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.init import db, bcrypt
from app.models import User, Permission
from app.utils.decorators import role_required, permission_required
from app.utils.hash_utils import hash_password
import json
import os

users_bp = Blueprint('users', __name__)

# Path to persistent user data file - same as auth.py uses
USERS_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'users_data.json')

def load_users_data():
    """Load users from JSON file"""
    try:
        if os.path.exists(USERS_DATA_FILE):
            with open(USERS_DATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading users data: {e}")
    return {}

def save_users_data(users_data):
    """Save users to JSON file"""
    try:
        os.makedirs(os.path.dirname(USERS_DATA_FILE), exist_ok=True)
        with open(USERS_DATA_FILE, 'w') as f:
            json.dump(users_data, f, indent=2)
    except Exception as e:
        print(f"Error saving users data: {e}")

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = load_users_data()
        return jsonify([{
            'id': u.get('id'),
            'username': username,
            'full_name': u.get('full_name'),
            'role': u.get('role'),
            'phone': u.get('phone'),
            'email': u.get('email'),
            'is_active': u.get('is_active', True),
            'modules': u.get('modules', ['dashboard'])
        } for username, u in users.items()])
    except Exception as e:
        return jsonify({'message': f'Error fetching users: {str(e)}'}), 500

@users_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    try:
        data = request.get_json()
        print(f"[DEBUG] Create user request data: {data}")
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        # Validate required fields
        if not data.get('username'):
            return jsonify({'message': 'Username is required'}), 400
        if not data.get('password'):
            return jsonify({'message': 'Password is required'}), 400
        
        # Load existing users
        users = load_users_data()
        
        if data['username'] in users:
            return jsonify({'message': 'Username already exists'}), 400
        
        # Validate role if provided
        valid_roles = ['superadmin', 'admin', 'reception', 'campaign', 'viewer']
        role = data.get('role', 'viewer')
        if role not in valid_roles:
            return jsonify({'message': f'Invalid role. Must be one of: {", ".join(valid_roles)}'}), 400
        
        # Validate email format if provided
        if data.get('email'):
            if '@' not in data.get('email', ''):
                return jsonify({'message': 'Invalid email format'}), 400
        
        # Generate next ID
        next_id = max([int(u.get('id', 0)) for u in users.values()] + [0]) + 1
        
        # Hash the password using SHA256
        password_hash, password_salt = hash_password(data['password'])
        
        # Create new user
        new_user = {
            'username': data['username'].strip(),
            'password_hash': password_hash,
            'password_salt': password_salt,
            'full_name': data.get('full_name', '').strip(),
            'role': role,
            'phone': data.get('phone', '').strip(),
            'email': data.get('email', '').strip(),
            'is_active': data.get('is_active', True),
            'modules': data.get('modules', ['dashboard']) if isinstance(data.get('modules'), list) else ['dashboard'],
            'id': next_id
        }
        
        # Add to users dict
        users[data['username'].strip()] = new_user
        
        # Save to file
        save_users_data(users)
        
        return jsonify({
            'message': 'User created successfully', 
            'id': next_id,
            'user': {
                'id': next_id,
                'username': new_user['username'],
                'full_name': new_user['full_name'],
                'role': new_user['role'],
                'email': new_user['email'],
                'phone': new_user['phone'],
                'is_active': new_user['is_active'],
                'modules': new_user['modules']
            }
        }), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error creating user: {str(e)}'}), 500

@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        users = load_users_data()
        for username, u in users.items():
            if u.get('id') == user_id:
                return jsonify({
                    'id': u.get('id'),
                    'username': username,
                    'full_name': u.get('full_name'),
                    'role': u.get('role'),
                    'phone': u.get('phone'),
                    'email': u.get('email'),
                    'is_active': u.get('is_active', True),
                    'modules': u.get('modules', ['dashboard'])
                })
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error fetching user: {str(e)}'}), 500

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        data = request.get_json()
        users = load_users_data()
        
        # Find user by ID
        target_username = None
        for username, u in users.items():
            if u.get('id') == user_id:
                target_username = username
                break
        
        if not target_username:
            return jsonify({'message': 'User not found'}), 404
        
        # Update user data
        if 'full_name' in data:
            users[target_username]['full_name'] = data['full_name']
        if 'role' in data:
            users[target_username]['role'] = data['role']
        if 'phone' in data:
            users[target_username]['phone'] = data['phone']
        if 'email' in data:
            users[target_username]['email'] = data['email']
        if 'password' in data and data['password']:
            # Hash the new password using SHA256
            password_hash, password_salt = hash_password(data['password'])
            users[target_username]['password_hash'] = password_hash
            users[target_username]['password_salt'] = password_salt
        if 'is_active' in data:
            users[target_username]['is_active'] = data['is_active']
        if 'modules' in data:
            users[target_username]['modules'] = data['modules']
        
        # Save changes
        save_users_data(users)
        
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating user: {str(e)}'}), 500

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        users = load_users_data()
        
        # Find and delete user by ID
        target_username = None
        for username, u in users.items():
            if u.get('id') == user_id:
                target_username = username
                break
        
        if not target_username:
            return jsonify({'message': 'User not found'}), 404
        
        del users[target_username]
        save_users_data(users)
        
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting user: {str(e)}'}), 500

@users_bp.route('/permissions', methods=['GET'])
@jwt_required()
@role_required(['superadmin', 'admin'])
def get_permissions():
    permissions = Permission.query.all()
    return jsonify([{
        'id': p.id,
        'role': p.role,
        'module': p.module,
        'can_read': p.can_read,
        'can_create': p.can_create,
        'can_update': p.can_update,
        'can_delete': p.can_delete
    } for p in permissions])

@users_bp.route('/sync-users', methods=['POST'])
@jwt_required()
def sync_users():
    """Sync users from frontend localStorage to backend"""
    try:
        data = request.get_json()
        users_list = data.get('users', [])
        
        if not users_list:
            return jsonify({'message': 'No users to sync'}), 400
        
        # Convert list to dict format (keyed by username)
        users_dict = {}
        for user in users_list:
            username = user.get('username')
            if username:
                # Hash password if provided, otherwise use existing hash
                if 'password' in user and user['password']:
                    password_hash, password_salt = hash_password(user['password'])
                else:
                    password_hash = user.get('password_hash', '')
                    password_salt = user.get('password_salt', '')
                
                users_dict[username] = {
                    'username': username,
                    'password_hash': password_hash,
                    'password_salt': password_salt,
                    'full_name': user.get('full_name', ''),
                    'role': user.get('role', 'viewer'),
                    'email': user.get('email', ''),
                    'phone': user.get('phone', ''),
                    'is_active': user.get('is_active', True),
                    'modules': user.get('modules', ['dashboard']),
                    'id': user.get('id', len(users_dict) + 100)
                }
        
        # Save synced users
        save_users_data(users_dict)
        
        return jsonify({
            'message': f'Synced {len(users_dict)} users successfully',
            'count': len(users_dict)
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error syncing users: {str(e)}'}), 500

@users_bp.route('/current-user/<username>', methods=['GET'])
@jwt_required()
def get_current_user(username):
    """Get latest user data by username - used for syncing logged-in user"""
    try:
        users = load_users_data()
        
        if username not in users:
            return jsonify({'message': 'User not found'}), 404
        
        u = users[username]
        return jsonify({
            'id': u.get('id'),
            'username': username,
            'full_name': u.get('full_name'),
            'role': u.get('role'),
            'phone': u.get('phone'),
            'email': u.get('email'),
            'is_active': u.get('is_active', True),
            'modules': u.get('modules', ['dashboard'])
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching user: {str(e)}'}), 500
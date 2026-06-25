from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.init import bcrypt, db
from app.models import User
from app.utils.hash_utils import verify_password
import json
import os

auth_bp = Blueprint('auth', __name__)

# Path to persistent user data file
USERS_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'users_data.json')

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

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    # DEBUG: Log what was received
    print(f"[DEBUG] Login attempt - Username: {username}, Password length: {len(password)}, Password first 50 chars: {password[:50]}")
    
    # Load users from JSON file
    users = load_users_data()
    
    # Check if user exists and password matches
    if username in users:
        user_data = users[username]
        
        # Check if user is active
        if not user_data.get('is_active', True):
            return jsonify({'error': 'User account is inactive'}), 401
        
        # Verify password using SHA256 hashing
        stored_hash = user_data.get('password_hash') or user_data.get('password')
        stored_salt = user_data.get('password_salt')
        
        print(f"[DEBUG] Stored hash length: {len(stored_hash)}, first 50 chars: {stored_hash[:50]}")
        print(f"[DEBUG] Password == stored_hash: {password == stored_hash}")
        
        # Method 2: Try hash password directly FIRST (TESTING METHOD - No salt needed)
        if password == stored_hash:
            # Password is the HASH ITSELF - for testing/development
            print(f"[DEBUG] Hash login successful for {username}")
            modules = user_data.get('modules', ['dashboard'])
            
            access_token = create_access_token(
                identity=username,
                additional_claims={
                    'id': user_data.get('id'),
                    'role': user_data.get('role'),
                    'modules': modules
                }
            )
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': user_data.get('id'),
                    'username': username,
                    'full_name': user_data.get('full_name'),
                    'role': user_data.get('role'),
                    'email': user_data.get('email'),
                    'modules': modules
                }
            })
        
        # Method 1: Try real password with SHA256 verification
        elif stored_salt and verify_password(password, stored_hash, stored_salt):
            # Password verified with SHA256 hashing (REAL PASSWORD METHOD)
            print(f"[DEBUG] Real password login successful for {username}")
            modules = user_data.get('modules', ['dashboard'])
            
            access_token = create_access_token(
                identity=username,
                additional_claims={
                    'id': user_data.get('id'),
                    'role': user_data.get('role'),
                    'modules': modules
                }
            )
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': user_data.get('id'),
                    'username': username,
                    'full_name': user_data.get('full_name'),
                    'role': user_data.get('role'),
                    'email': user_data.get('email'),
                    'modules': modules
                }
            })
        
        # Method 3: If password is plain text (old format), verify directly
        elif stored_salt is None and isinstance(stored_hash, str) and len(stored_hash) < 64:
            # This is a plain text password, verify directly
            if password == stored_hash:
                modules = user_data.get('modules', ['dashboard'])
                access_token = create_access_token(
                    identity=username,
                    additional_claims={
                        'id': user_data.get('id'),
                        'role': user_data.get('role'),
                        'modules': modules
                    }
                )
                return jsonify({
                    'access_token': access_token,
                    'user': {
                        'id': user_data.get('id'),
                        'username': username,
                        'full_name': user_data.get('full_name'),
                        'role': user_data.get('role'),
                        'email': user_data.get('email'),
                        'modules': modules
                    }
                })
    
    # Try database if test users don't match
    try:
        user = User.query.filter_by(username=username, is_active=True).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            modules = user.get_modules()
            
            access_token = create_access_token(
                identity=user.username,
                additional_claims={
                    'id': user.id,
                    'role': user.role,
                    'modules': modules
                }
            )
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'role': user.role,
                    'email': user.email,
                    'modules': modules
                }
            })
    except Exception as e:
        # Database not available, will use test users only
        pass
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_token})
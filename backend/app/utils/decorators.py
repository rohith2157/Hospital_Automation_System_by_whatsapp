from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models import Permission

def role_required(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] not in required_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def permission_required(module, action):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            
            # Superadmin has all permissions
            if current_user['role'] == 'superadmin':
                return f(*args, **kwargs)
            
            # Check permission in database
            permission = Permission.query.filter_by(
                role=current_user['role'],
                module=module
            ).first()
            
            if not permission:
                return jsonify({'error': 'Permission denied'}), 403
            
            # Check specific action
            action_map = {
                'read': permission.can_read,
                'create': permission.can_create,
                'update': permission.can_update,
                'delete': permission.can_delete
            }
            
            if not action_map.get(action, False):
                return jsonify({'error': 'Permission denied'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
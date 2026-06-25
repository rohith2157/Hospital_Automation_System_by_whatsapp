from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.init import db
from app.models import Branch

branches_bp = Blueprint('branches', __name__)

@branches_bp.route('/branches', methods=['GET'])
@jwt_required()
def get_branches():
    branches = Branch.query.all()
    return jsonify([{
        'id': branch.id,
        'name': branch.name,
        'address': branch.address,
        'phone': branch.phone,
        'timezone': branch.timezone,
        'created_at': branch.created_at.isoformat() if branch.created_at else None
    } for branch in branches])

@branches_bp.route('/branches/<int:branch_id>', methods=['GET'])
@jwt_required()
def get_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    return jsonify({
        'id': branch.id,
        'name': branch.name,
        'address': branch.address,
        'phone': branch.phone,
        'timezone': branch.timezone,
        'created_at': branch.created_at.isoformat() if branch.created_at else None
    })
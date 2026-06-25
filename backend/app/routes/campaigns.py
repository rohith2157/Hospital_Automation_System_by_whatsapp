from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.init import db
from app.models import Campaign, Branch
from app.utils.decorators import permission_required

campaigns_bp = Blueprint('campaigns', __name__)

@campaigns_bp.route('/campaigns', methods=['GET'])
@jwt_required()
@permission_required('campaigns', 'read')
def get_campaigns():
    campaigns = Campaign.query.all()
    
    return jsonify([{
        'id': camp.id,
        'name': camp.name,
        'branch_id': camp.branch_id,
        'target_criteria': camp.target_criteria,
        'message_template': camp.message_template,
        'scheduled_at': camp.scheduled_at.isoformat() if camp.scheduled_at else None,
        'status': camp.status,
        'stats': camp.stats,
        'created_by': camp.created_by,
        'created_at': camp.created_at.isoformat() if camp.created_at else None,
        'branch_name': camp.branch.name if camp.branch else None
    } for camp in campaigns])

@campaigns_bp.route('/campaigns', methods=['POST'])
@jwt_required()
@permission_required('campaigns', 'create')
def create_campaign():
    data = request.get_json()
    current_user = get_jwt_identity()
    
    campaign = Campaign(
        name=data['name'],
        branch_id=data.get('branch_id'),
        target_criteria=data.get('target_criteria', {}),
        message_template=data['message_template'],
        scheduled_at=datetime.fromisoformat(data['scheduled_at'].replace('Z', '+00:00')) if data.get('scheduled_at') else None,
        status=data.get('status', 'draft'),
        created_by=current_user['id']
    )
    
    db.session.add(campaign)
    db.session.commit()
    
    return jsonify({
        'message': 'Campaign created successfully',
        'id': campaign.id
    }), 201

@campaigns_bp.route('/campaigns/<int:campaign_id>/send', methods=['POST'])
@jwt_required()
@permission_required('campaigns', 'create')
def send_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    
    # TODO: Implement campaign sending logic
    # This would typically queue the campaign for sending via Celery
    
    campaign.status = 'scheduled'
    db.session.commit()
    
    return jsonify({'message': 'Campaign queued for sending'})
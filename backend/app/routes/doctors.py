from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.init import db
from app.models import Doctor, Branch
from app.utils.decorators import permission_required

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/doctors', methods=['GET'])
# @jwt_required()  # Temporarily disabled
def get_doctors():
    doctors = Doctor.query.all()
    
    return jsonify([{
        'id': doc.id,
        'name': f"{doc.first_name} {doc.last_name}",
        'specialization': doc.specialties,
        'branch_id': doc.branch_id
    } for doc in doctors]), 200

@doctors_bp.route('/doctors', methods=['POST'])
# @jwt_required()  # Temporarily disabled
def create_doctor():
    data = request.get_json()
    
    name_parts = data['name'].split(' ', 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    doctor = Doctor(
        branch_id=data['branch_id'],
        first_name=first_name,
        last_name=last_name,
        specialties=data.get('specialization'),
        is_active=True
    )
    
    db.session.add(doctor)
    db.session.commit()
    
    return jsonify({
        'message': 'Doctor created successfully',
        'id': doctor.id
    }), 201


@doctors_bp.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify({
        'id': doctor.id,
        'name': f"{doctor.first_name} {doctor.last_name}",
        'first_name': doctor.first_name,
        'last_name': doctor.last_name,
        'specialization': doctor.specialties,
        'branch_id': doctor.branch_id,
        'is_active': doctor.is_active,
        'consultation_fee': float(doctor.consultation_fee) if doctor.consultation_fee else None
    }), 200


@doctors_bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    data = request.get_json()
    
    if 'name' in data:
        name_parts = data['name'].split(' ', 1)
        doctor.first_name = name_parts[0]
        doctor.last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    if 'first_name' in data:
        doctor.first_name = data['first_name']
    if 'last_name' in data:
        doctor.last_name = data['last_name']
    if 'specialization' in data:
        doctor.specialties = data['specialization']
    if 'branch_id' in data:
        doctor.branch_id = data['branch_id']
    if 'is_active' in data:
        doctor.is_active = data['is_active']
    if 'consultation_fee' in data:
        doctor.consultation_fee = data['consultation_fee']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Doctor updated successfully',
        'id': doctor.id
    }), 200


@doctors_bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    
    db.session.delete(doctor)
    db.session.commit()
    
    return jsonify({
        'message': 'Doctor deleted successfully'
    }), 200
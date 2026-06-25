from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.init import db
from app.models import Patient
from app.utils.decorators import permission_required

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients', methods=['GET'])
@jwt_required()
def get_patients():
    patients = Patient.query.all()
    return jsonify([{
        'id': p.id,
        'phone': p.whatsapp_number,
        'name': p.name,
        'age': p.age,
        'gender': p.gender,
        'last_visit': p.last_visit.isoformat() if p.last_visit else None,
        'created_at': p.created_at.isoformat() if p.created_at else None
    } for p in patients]), 200

@patients_bp.route('/patients', methods=['POST'])
@jwt_required()
def create_patient():
    from datetime import datetime
    data = request.get_json()
    
    patient = Patient(
        whatsapp_number=data.get('phone'),
        name=data['name'],
        age=data.get('age'),
        gender=data.get('gender'),
        extra=data.get('extra', {})
    )
    
    db.session.add(patient)
    db.session.commit()
    
    return jsonify({'message': 'Patient added successfully', 'id': patient.id}), 201
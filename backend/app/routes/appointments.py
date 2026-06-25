from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_
from datetime import datetime, date, timedelta
from app.init import db
from app.models import Appointment, Patient, Doctor, Branch
from app.utils.decorators import permission_required

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointments', methods=['GET'])
# @jwt_required()  # Temporarily disabled for n8n testing
def get_appointments():
    appointments = Appointment.query.order_by(Appointment.scheduled_at.desc()).all()
    
    return jsonify([{
        'id': apt.id,
        'patient': apt.patient_name,
        'patient_phone': apt.patient_phone,
        'doctor': f"{apt.doctor.first_name} {apt.doctor.last_name}" if apt.doctor else 'Unknown',
        'date': apt.scheduled_at.strftime('%Y-%m-%d') if apt.scheduled_at else None,
        'time': apt.scheduled_at.strftime('%H:%M') if apt.scheduled_at else None,
        'status': apt.status
    } for apt in appointments]), 200

@appointments_bp.route('/appointments', methods=['POST'])
# @jwt_required()  # Temporarily disabled for testing
def create_appointment():
    data = request.get_json()
    
    # Handle both date/time format and scheduled_at format
    if 'scheduled_at' in data:
        scheduled_datetime = datetime.fromisoformat(data['scheduled_at'].replace('Z', '+00:00'))
    else:
        scheduled_datetime = datetime.strptime(f"{data['date']} {data['time']}", '%Y-%m-%d %H:%M')
    
    appointment = Appointment(
        branch_id=data.get('branch_id', 1),
        doctor_id=data['doctor_id'],
        patient_name=data.get('patient_name', data.get('patient')),
        patient_phone=data.get('patient_phone'),
        scheduled_at=scheduled_datetime,
        status='booked',
        source=data.get('source', 'admin')  # Valid values: whatsapp, admin, phone
    )
    
    db.session.add(appointment)
    db.session.commit()
    
    return jsonify({
        'message': 'Appointment created successfully',
        'id': appointment.id
    }), 201

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['GET'])
@jwt_required()
@permission_required('appointments', 'read')
def get_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    return jsonify({
        'id': appointment.id,
        'branch_id': appointment.branch_id,
        'doctor_id': appointment.doctor_id,
        'patient_id': appointment.patient_id,
        'patient_name': appointment.patient_name,
        'patient_phone': appointment.patient_phone,
        'scheduled_at': appointment.scheduled_at.isoformat() if appointment.scheduled_at else None,
        'status': appointment.status,
        'source': appointment.source,
        'created_at': appointment.created_at.isoformat() if appointment.created_at else None,
        'updated_at': appointment.updated_at.isoformat() if appointment.updated_at else None
    })

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
@jwt_required()
@permission_required('appointments', 'update')
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.get_json()
    
    if 'branch_id' in data:
        appointment.branch_id = data['branch_id']
    if 'doctor_id' in data:
        appointment.doctor_id = data['doctor_id']
    if 'patient_name' in data:
        appointment.patient_name = data['patient_name']
    if 'patient_phone' in data:
        appointment.patient_phone = data['patient_phone']
    if 'scheduled_at' in data:
        appointment.scheduled_at = datetime.fromisoformat(data['scheduled_at'].replace('Z', '+00:00'))
    if 'status' in data:
        appointment.status = data['status']
    
    db.session.commit()
    
    return jsonify({'message': 'Appointment updated successfully'})

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
# @jwt_required()
# @permission_required('appointments', 'delete')
def delete_appointment(appointment_id):
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        
        db.session.delete(appointment)
        db.session.commit()
        
        return jsonify({'message': 'Appointment deleted successfully', 'id': appointment_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@appointments_bp.route('/appointments/upcoming', methods=['GET'])
def get_upcoming_appointments():
    """Get all appointments happening within the next 24 hours for 2-hour reminder workflow"""
    try:
        now = datetime.now()
        next_24_hours = now + timedelta(hours=24)

        appointments = Appointment.query.filter(
            Appointment.scheduled_at >= now,
            Appointment.scheduled_at <= next_24_hours
        ).all()

        result = []
        for apt in appointments:
            result.append({
                "id": apt.id,
                "patient": apt.patient_name,
                "phone": apt.patient_phone,
                "doctor": f"{apt.doctor.first_name} {apt.doctor.last_name}" if apt.doctor else None,
                "date": apt.scheduled_at.strftime("%Y-%m-%d") if apt.scheduled_at else None,
                "time": apt.scheduled_at.strftime("%H:%M") if apt.scheduled_at else None,
                "scheduled_at": apt.scheduled_at.isoformat() if apt.scheduled_at else None,
                "status": apt.status
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
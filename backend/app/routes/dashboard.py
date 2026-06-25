from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from datetime import date
from app.init import db
from app.models import Patient, Appointment

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/summary', methods=['GET'])
# @jwt_required()
def get_dashboard_summary():
    # Count total patients
    total_patients = Patient.query.count()
    
    # Count total appointments
    total_appointments = Appointment.query.count()
    
    # Count today's appointments
    today = date.today()
    appointments_today = Appointment.query.filter(
        func.date(Appointment.scheduled_at) == today
    ).count()
    
    return jsonify({
        'totalPatients': total_patients,
        'totalAppointments': total_appointments,
        'appointmentsToday': appointments_today
    }), 200

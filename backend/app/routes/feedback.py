from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import and_
from datetime import datetime
from app.init import db
from app.models import Feedback, Appointment, Doctor, Branch
from app.utils.decorators import permission_required

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET'])
@jwt_required()
@permission_required('feedback', 'read')
def get_feedback():
    branch_id = request.args.get('branch_id')
    doctor_id = request.args.get('doctor_id')
    feedback_date = request.args.get('date')
    
    query = db.session.query(Feedback).join(Appointment)
    
    if branch_id:
        query = query.filter(Appointment.branch_id == branch_id)
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if feedback_date:
        try:
            target_date = datetime.strptime(feedback_date, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Feedback.created_at) == target_date)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    feedbacks = query.all()
    
    return jsonify([{
        'id': fb.id,
        'appointment_id': fb.appointment_id,
        'patient_id': fb.patient_id,
        'type': fb.type,
        'rating': fb.rating,
        'comments': fb.comments,
        'category': fb.category,
        'created_at': fb.created_at.isoformat() if fb.created_at else None,
        'patient_name': fb.patient.name if fb.patient else None,
        'doctor_name': f"{fb.appointment.doctor.first_name} {fb.appointment.doctor.last_name}" if fb.appointment and fb.appointment.doctor else None
    } for fb in feedbacks])

@feedback_bp.route('/feedback', methods=['POST'])
@jwt_required()
def create_feedback():
    data = request.get_json()
    
    feedback = Feedback(
        appointment_id=data.get('appointment_id'),
        patient_id=data.get('patient_id'),
        type=data['type'],
        rating=data.get('rating'),
        comments=data.get('comments'),
        category=data.get('category')
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    return jsonify({
        'message': 'Feedback submitted successfully',
        'id': feedback.id
    }), 201

# ==================== OPD FEEDBACK (New) ====================

@feedback_bp.route('/feedback/opd', methods=['POST'])
def create_opd_feedback():
    """Create OPD feedback after appointment"""
    data = request.get_json()
    
    try:
        db.session.execute("""
            INSERT INTO opd_feedback 
            (appointment_id, doctor_rating, waiting_time_rating, overall_rating, comments)
            VALUES (:appt_id, :doctor, :waiting, :overall, :comments)
        """, {
            'appt_id': data.get('appointment_id'),
            'doctor': data.get('doctor_rating'),
            'waiting': data.get('waiting_time_rating'),
            'overall': data.get('overall_rating'),
            'comments': data.get('comments', '')
        })
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'OPD feedback submitted successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@feedback_bp.route('/feedback/opd', methods=['GET'])
def get_opd_feedback():
    """Get all OPD feedback"""
    try:
        results = db.session.execute("""
            SELECT 
                f.id, f.appointment_id, f.doctor_rating, f.waiting_time_rating,
                f.overall_rating, f.comments, f.created_at,
                a.patient_name, CONCAT(d.first_name, ' ', d.last_name) as doctor_name
            FROM opd_feedback f
            LEFT JOIN appointments a ON f.appointment_id = a.id
            LEFT JOIN doctors d ON a.doctor_id = d.id
            ORDER BY f.created_at DESC
        """).fetchall()
        
        feedback_list = []
        for row in results:
            feedback_list.append({
                'id': row[0],
                'appointment_id': row[1],
                'doctor_rating': row[2],
                'waiting_time_rating': row[3],
                'overall_rating': row[4],
                'comments': row[5],
                'created_at': row[6].isoformat() if row[6] else None,
                'patient_name': row[7],
                'doctor_name': row[8]
            })
        
        return jsonify(feedback_list), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ==================== IPD FEEDBACK (New) ====================

@feedback_bp.route('/feedback/ipd', methods=['POST'])
def create_ipd_feedback():
    """Create IPD feedback for admitted patients"""
    data = request.get_json()
    
    try:
        db.session.execute("""
            INSERT INTO ipd_feedback 
            (patient_id, room_cleanliness, nursing_care, doctor_visit, food_quality, overall_rating, comments)
            VALUES (:patient_id, :room, :nursing, :doctor, :food, :overall, :comments)
        """, {
            'patient_id': data.get('patient_id'),
            'room': data.get('room_cleanliness'),
            'nursing': data.get('nursing_care'),
            'doctor': data.get('doctor_visit'),
            'food': data.get('food_quality'),
            'overall': data.get('overall_rating'),
            'comments': data.get('comments', '')
        })
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'IPD feedback submitted successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@feedback_bp.route('/feedback/ipd', methods=['GET'])
def get_ipd_feedback():
    """Get all IPD feedback"""
    try:
        results = db.session.execute("""
            SELECT 
                f.id, f.patient_id, f.room_cleanliness, f.nursing_care,
                f.doctor_visit, f.food_quality, f.overall_rating, f.comments,
                f.created_at, p.name as patient_name
            FROM ipd_feedback f
            LEFT JOIN patients p ON f.patient_id = p.id
            ORDER BY f.created_at DESC
        """).fetchall()
        
        feedback_list = []
        for row in results:
            feedback_list.append({
                'id': row[0],
                'patient_id': row[1],
                'room_cleanliness': row[2],
                'nursing_care': row[3],
                'doctor_visit': row[4],
                'food_quality': row[5],
                'overall_rating': row[6],
                'comments': row[7],
                'created_at': row[8].isoformat() if row[8] else None,
                'patient_name': row[9]
            })
        
        return jsonify(feedback_list), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
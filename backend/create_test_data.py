from app import create_app
from app.models import Appointment, Patient, Doctor
from datetime import datetime, timedelta
from app.init import db

app = create_app()

with app.app_context():
    # Create test patient
    patient = Patient(
        phone="9876543210",
        name="John Doe",
        age=35,
        gender="Male"
    )
    db.session.add(patient)
    db.session.commit()
    
    # Create test appointments
    tomorrow = datetime.now() + timedelta(days=1)
    
    apt1 = Appointment(
        patient_id=patient.id,
        patient_name=patient.name,
        doctor_id=1,  # Assuming doctor with ID 1 exists
        scheduled_at=tomorrow.replace(hour=10, minute=0),
        status='confirmed'
    )
    
    apt2 = Appointment(
        patient_id=patient.id,
        patient_name=patient.name,
        doctor_id=1,
        scheduled_at=tomorrow.replace(hour=14, minute=30),
        status='pending'
    )
    
    db.session.add(apt1)
    db.session.add(apt2)
    db.session.commit()
    
    print(f"✅ Created 2 test appointments for tomorrow!")
    print(f"   - 10:00 AM - {patient.name}")
    print(f"   - 02:30 PM - {patient.name}")

from app import create_app
from app.models import Doctor
from app.init import db

app = create_app()

with app.app_context():
    # Create test doctors
    doctors = [
        Doctor(first_name="John", last_name="Smith", specialization="Cardiology", branch_id=1),
        Doctor(first_name="Sarah", last_name="Johnson", specialization="Pediatrics", branch_id=1),
        Doctor(first_name="Michael", last_name="Brown", specialization="Orthopedics", branch_id=1),
    ]
    
    for doctor in doctors:
        db.session.add(doctor)
    
    db.session.commit()
    
    print("✅ Created 3 test doctors:")
    for d in doctors:
        print(f"   - Dr. {d.first_name} {d.last_name} ({d.specialization})")

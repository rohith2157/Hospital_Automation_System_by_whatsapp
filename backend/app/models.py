from app.init import db
from datetime import datetime
import json

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    password_salt = db.Column(db.String(255), nullable=True)
    full_name = db.Column(db.String(255))
    role = db.Column(db.Enum('superadmin','admin','reception','campaign','viewer'), 
                    nullable=False, default='viewer')
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())
    
    # Add password property for backward compatibility
    @property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self, value):
        self.password_hash = value
    
    def get_modules(self):
        """Get modules safely, default to dashboard if not set"""
        # For now, return all modules for all users until DB column is added
        return ['dashboard', 'appointments', 'patients', 'doctors', 'users']

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    module = db.Column(db.String(100), nullable=False)
    can_read = db.Column(db.Boolean, default=False)
    can_create = db.Column(db.Boolean, default=False)
    can_update = db.Column(db.Boolean, default=False)
    can_delete = db.Column(db.Boolean, default=False)

class Branch(db.Model):
    __tablename__ = 'branches'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(50))
    timezone = db.Column(db.String(50), default='Asia/Kolkata')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    specialties = db.Column(db.String(255))
    consultation_fee = db.Column(db.Numeric(10, 2))
    is_active = db.Column(db.Boolean, default=True)
    
    branch = db.relationship('Branch', backref=db.backref('doctors', lazy=True))

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    whatsapp_number = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('male','female','other'))
    last_visit = db.Column(db.Date)
    extra = db.Column(db.JSON)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    patient_name = db.Column(db.String(255))
    patient_phone = db.Column(db.String(30))
    scheduled_at = db.Column(db.DateTime)
    status = db.Column(db.Enum('booked','confirmed','cancelled','completed','no_show'), 
                      default='booked')
    source = db.Column(db.Enum('whatsapp','admin','phone'), default='whatsapp')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())
    
    branch = db.relationship('Branch')
    doctor = db.relationship('Doctor')
    patient = db.relationship('Patient')
    creator = db.relationship('User')

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    type = db.Column(db.Enum('opd','ipd'))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)
    category = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    
    appointment = db.relationship('Appointment')
    patient = db.relationship('Patient')

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    target_criteria = db.Column(db.JSON)
    message_template = db.Column(db.Text)
    scheduled_at = db.Column(db.DateTime)
    status = db.Column(db.Enum('draft','scheduled','running','completed','cancelled'), 
                      default='draft')
    stats = db.Column(db.JSON, default=lambda: {})
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    
    branch = db.relationship('Branch')
    creator = db.relationship('User')

class MessageLog(db.Model):
    __tablename__ = 'message_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    to_number = db.Column(db.String(30))
    from_number = db.Column(db.String(30))
    message_type = db.Column(db.String(50))
    body = db.Column(db.Text)
    direction = db.Column(db.Enum('outbound','inbound'))
    status = db.Column(db.String(50))
    provider_message_id = db.Column(db.String(255))
    msg_metadata = db.Column(db.JSON)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Additional MySQL tables
class LoginDetails(db.Model):
    __tablename__ = 'login_details'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    login_time = db.Column(db.DateTime)
    logout_time = db.Column(db.DateTime)
    ip_address = db.Column(db.String(50))
    device_info = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class ModuleCreation(db.Model):
    __tablename__ = 'module_creation'
    
    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))
    route = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class SubModuleCreation(db.Model):
    __tablename__ = 'sub_module_creation'
    
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module_creation.id'))
    sub_module_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    route = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class RoleCreation(db.Model):
    __tablename__ = 'role_creation'
    
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class RoleAssign(db.Model):
    __tablename__ = 'role_assign'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role_creation.id'))
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class UsersRole(db.Model):
    __tablename__ = 'users_role'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role_creation.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
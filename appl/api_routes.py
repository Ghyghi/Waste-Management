from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'household', 'service', 'admin'
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50))  # Column for polymorphic identity

    schedules = db.relationship('WasteCollectionSchedule', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __repr__(self):
        return f'<User id={self.id} username={self.username} role={self.role}>'

class Credentials(User):
    __tablename__ = 'credentials'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'credentials',
        'inherit_condition': (id == User.id)
    }

    def __repr__(self):
        return f'<Credentials id={self.id} email={self.email}>'

class WasteCollection(db.Model):
    __tablename__ = 'waste_collection'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'scheduled', 'in_progress', 'completed', 'cancelled', 'missed', 'delayed'
    waste_type_id = db.Column(db.Integer, db.ForeignKey('waste_type.id'), nullable=False)
    location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User id={self.user_id} Collection id={self.id} status={self.status}>'

class RecyclingEffort(db.Model):
    __tablename__ = 'recycling_effort'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    waste_type_id = db.Column(db.Integer, db.ForeignKey('waste_type.id'), nullable=False)

    waste_type = db.relationship('WasteType', backref=db.backref('efforts', lazy=True))

    def __repr__(self):
        return f'<RecyclingEffort id={self.id} date={self.date} Waste Type={self.waste_type_id}>'

class WasteType(db.Model):
    __tablename__ = 'waste_type'
    
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<WasteType id={self.id} name={self.name}>'

class Location(db.Model):  # Changed from Locations to Location
    __tablename__ = 'location'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # Changed from locations to name

    def __repr__(self):
        return f'<Location id={self.id} name={self.name}>'

class WasteCollectionSchedule(db.Model):
    __tablename__ = 'waste_collection_schedule'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    collection_date = db.Column(db.DateTime, nullable=False)
    waste_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='scheduled')  # 'scheduled', 'completed', etc.
    notified = db.Column(db.Boolean, default=False)  # For reminder notifications

    def __repr__(self):
        return f'<WasteCollectionSchedule id={self.id} user_id={self.user_id} Waste type={self.waste_type} Status={self.status}>'

class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(50), nullable=False)  # 'reminder', 'confirmation', 'update', 'deletion'

    def __repr__(self):
        return f'<Notification id={self.id} user_id={self.user_id} Message={self.message} Type={self.type}>'

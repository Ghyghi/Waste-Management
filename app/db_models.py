from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'household', 'service', 'admin'
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
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
    __tablename__ = 'wastecollection'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'scheduled', 'in_progress', 'completed', 'cancelled', 'missed', 'delayed'
    waste_type_id = db.Column(db.Integer, db.ForeignKey('wastetype.id'), nullable=False) # 'general waste' , 'recylable', 'non-recyclable'
    location = db.Column(db.String(50), nullable=False)

class RecyclingEffort(db.Model):
    __tablename__ = 'recyclingtracker'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    waste_type_id = db.Column(db.Integer, db.ForeignKey('wastetype.id'), nullable=False)

class WasteType(db.Model):
    __tablename__ = 'wastetype'
    
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Locations(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    locations = db.Column(db.String(50), nullable=False)

class WasteCollectionSchedule(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    collection_date = db.Column(db.DateTime, nullable=False)
    waste_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='scheduled')  # 'scheduled', 'completed', etc.
    notified = db.Column(db.Boolean, default=False)  # For reminder notifications

    user = db.relationship('User', backref=db.backref('schedules', lazy=True))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(50), nullable=False)  # 'reminder', 'confirmation', 'update', 'deletion'

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String(80), primary_key=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'household', 'service', 'admin'
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50))  # Column for polymorphic identity

    user_schedules_rel = db.relationship('WasteCollectionSchedule', backref='user_rel', lazy=True)
    user_notifications_rel = db.relationship('Notification', backref='user_rel', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __repr__(self):
        return f'<username={self.username} role={self.role}>'


class WasteCollection(db.Model):
    __tablename__ = 'wastecollection'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'scheduled', 'in_progress', 'completed', 'cancelled', 'missed', 'delayed'
    waste_type = db.Column(db.Integer, db.ForeignKey('wastetype.id'), nullable=False)
    location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<WasteCollection id={self.id} username={self.username} status={self.status}>'

class RecyclingEffort(db.Model):
    __tablename__ = 'recyclingeffort'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    waste_name = db.Column(db.String(55), db.ForeignKey('wastetype.name'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<RecyclingEffort id={self.id} username={self.username} date={self.date} waste_name={self.waste_name}>'

class WasteType(db.Model):
    __tablename__ = 'wastetype'

    id = db.Column(db.Integer, unique=True , primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<WasteType id={self.id} name={self.name}>'

class Locations(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(55), unique=True, nullable=False)

    def __repr__(self):
        return f'<Location id={self.id} name={self.name}>'

class WasteCollectionSchedule(db.Model):
    __tablename__ = 'waste_collection_schedule'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    collection_date = db.Column(db.DateTime, nullable=False)
    waste_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='scheduled')  # 'scheduled', 'completed', etc.
    notified = db.Column(db.Boolean, default=False)  # For reminder notifications
    location = db.Column(db.String(50), nullable=False)

    user_nrel = db.relationship('User', backref='waste_collection_schedules', lazy=True)

    def __repr__(self):
        return f'<WasteCollectionSchedule id={self.id} username={self.username} collection_date={self.collection_date} status={self.status}>'

class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(50), nullable=False)  # 'reminder', 'confirmation', 'update', 'deletion'

    user_nrel = db.relationship('User', backref='notifications_rel', lazy=True)

    def __repr__(self):
        return f'<Notification id={self.id} username={self.username} message={self.message} type={self.type}>'
    

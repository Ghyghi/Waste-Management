from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'household', 'service', 'admin'
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))  # Column for polymorphic identity

    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': type
    }

    def __repr__(self):
        return f'<User id={self.id} username={self.username} role={self.role}>'

class Credentials(User):
    __tablename__ = 'credentials'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'credentials',
        'inherit_condition': (id == User.id)
    }
    def __repr__(self):
        return f'<Credentials id={self.id} email={self.email}>'

class WasteCollection(db.Model):
    __tablename__ = 'wastecollection'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'scheduled', 'in_progress', 'completed', 'cancelled', 'missed', 'delayed'
    waste_type_id = db.Column(db.Integer, db.ForeignKey('wastetype.id'), nullable=False) # 'general waste' , 'recylable', 'non-recyclable'
    location = db.Column(db.String(50), nullable=False)

class RecyclingEffort(db.Model):
    __tablename__ = 'recyclingtracker'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, unique=True, autoincrement=True)
    firstname = db.Column(db.String(150), unique=True, nullable=False)
    secondname = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), primary_key=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
# app/config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/Smart_Waste'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

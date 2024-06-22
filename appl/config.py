class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/Smart_Waste'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
# Application security
    SECRET_KEY = 'your_secret_key'

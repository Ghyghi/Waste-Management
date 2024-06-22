from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import os

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('appl.config.Config')  

    db.init_app(app)
    migrate.init_app(app, db) 
    mail.init_app(app)

    with app.app_context():
        
        import appl.db_models  
        from .api_routes import register_routes  

        register_routes(app) 

        create_database()

    return app

def create_database():
   
    with db.engine.connect() as connection:
        db.reflect()  
        db.create_all() 

        print('Database created!')

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
    app.config.from_object('appl.config.Config')  # Load configuration from config.py

    # Initialize extensions with the Flask application
    db.init_app(app)
    migrate.init_app(app, db) 
    mail.init_app(app)

    with app.app_context():
<<<<<<< HEAD
        # Import models and register routes 
        import appl.db_models
        from .api_routes import register_routes
=======
        # Import models and register routes within the app context to avoid circular imports
        import appl.db_models  # Importing models
        from .api_routes import register_routes  # Assuming you have a module for API routes
>>>>>>> f5f0d87b1a32c5261e59d961517dcec6aec3436c

        register_routes(app)  # Registering routes

        # Ensure the database is created (if not already exists)
        create_database()

        return app

def create_database():
    # Create database tables if they don't exist
    with db.engine.connect() as connection:
        db.reflect()  # Reflect the existing database tables
        db.create_all()  # Create all tables defined in the models

        print('Database created!')

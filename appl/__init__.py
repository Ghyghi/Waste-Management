from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import os


migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('appl.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    with app.app_context():
        # Import models and register routes within the app context
        import appl.db_models
        from .api_routes import register_routes

        register_routes(app)

        # Ensure the database is created (if not already exists)
        create_database()

        return app

def create_database():
    # Create database tables if they don't exist
    with db.engine.connect() as connection:
        if not db.engine.dialect.has_table(connection, 'your_table_name'):
            db.create_all()
            print('Database created!')

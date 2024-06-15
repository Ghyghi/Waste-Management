from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        from .db_models import User, WasteCollection, RecyclingEffort, Locations  
        from .api_routes import register_routes

        register_routes(app)

        db.create_all()

        return app
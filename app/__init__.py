from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from .db_models import User, WasteCollection, RecyclingEffort, Locations  
    from .api_routes import register_routes

    register_routes(app)

    with app.app_context():
        db.create_all()

    return app

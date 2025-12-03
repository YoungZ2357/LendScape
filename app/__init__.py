from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import Config
from supabase import create_client, Client
import os
from flask_cors import CORS

db = SQLAlchemy()
supabase_client: Client = None


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    global supabase_client
    supabase_client = create_client(
        app.config['SUPABASE_URL'],
        app.config['SUPABASE_ANON_KEY'],
    )


    from app.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.item import items_bp
    app.register_blueprint(items_bp)

    from app.users import users_bp
    app.register_blueprint(users_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.locations import locations_bp
    app.register_blueprint(locations_bp)

    from app.request import requests_bp
    app.register_blueprint(requests_bp)

    from app.order import orders_bp
    app.register_blueprint(orders_bp)

    from app.review import reviews_bp
    app.register_blueprint(reviews_bp)

    from app.stats import stats_bp
    app.register_blueprint(stats_bp)

    with app.app_context():
        db.create_all()


    return app
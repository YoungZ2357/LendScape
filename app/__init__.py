from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.item import items_bp
    app.register_blueprint(items_bp)

    from app.users import users_bp
    app.register_blueprint(users_bp)

    with app.app_context():
        db.create_all()


    return app
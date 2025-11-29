from flask import Blueprint

locations_bp = Blueprint('locations', __name__)

from app.locations import routes
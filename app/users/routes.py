from flask import Blueprint, request, jsonify
from app import db
from app.users import users_bp
from app.models import User, Item
from decimal import Decimal


@users_bp.route('/users/', methods=['GET'])
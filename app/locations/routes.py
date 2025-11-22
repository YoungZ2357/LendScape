# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ProjectName: LendScape
# FileName: routes.py
# Date: 2025/11/19 13:34
# -------------------------------------------------------------------------
from flask import Blueprint, render_template, jsonify
from app.models import Location
from app.auth.decorators import require_auth

locations_bp = Blueprint('locations', __name__)

@locations_bp.route('/locations/add')
@require_auth
def add_location_page():
    return render_template('locations/add_location.html')


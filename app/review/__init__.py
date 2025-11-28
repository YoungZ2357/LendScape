# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ProjectName: LendScape
# FileName: __init__.py.py
# Date: 2025/11/28 16:10
# -------------------------------------------------------------------------
from flask import Blueprint

reviews_bp = Blueprint('reviews', __name__)

from app.review import routes
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ProjectName: LendScape
# FileName: __init__.py.py
# Date: 2025/11/26 18:26
# -------------------------------------------------------------------------
from flask import Blueprint

requests_bp = Blueprint('requests', __name__)

from app.request import routes
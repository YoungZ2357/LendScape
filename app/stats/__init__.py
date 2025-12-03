# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ProjectName: LendScape
# FileName: __init__.py.py
# Date: 2025/12/2 11:30
# -------------------------------------------------------------------------
from flask import Blueprint

stats_bp = Blueprint('stats', __name__)

from app.stats import routes
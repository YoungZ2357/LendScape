# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ProjectName: LendScape
# FileName: __init__.py.py
# Date: 2025/11/28 11:04
# -------------------------------------------------------------------------
from flask import Blueprint

orders_bp = Blueprint('orders', __name__)

from app.order import routes
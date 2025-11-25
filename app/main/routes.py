from flask import Blueprint, render_template, request, jsonify, session
from app.models import User
bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    current_user = None

    if 'user_id' in session:
        current_user = User.query.filter_by(userId=session['user_id']).first()

        if not current_user:
            session.clear()

    return render_template("index.html",
                           current_user=current_user
                           )
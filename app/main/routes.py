from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    return render_template("index.html")
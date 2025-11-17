from flask import Blueprint, request, jsonify, render_template
from app import db
from app.users import users_bp
from sqlalchemy import or_
from app.models import User, Location
from decimal import Decimal

@users_bp.route('/users/search', methods=['GET'])
def search_page():
    return render_template("demo_user.html")

@users_bp.route('/api/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 8, type=int)

    kw = request.args.get("search", "", type=str)

    query = User.query
    if kw:
        conditions = [
            User.firstName.ilike(f"%{kw}%"),
            User.lastName.ilike(f"%{kw}%"),
            User.email.ilike(f"%{kw}%")
        ]
        query = query.filter(or_(*conditions))

    pagination = query.paginate(page=page, per_page=size, error_out=False)
    print(query)
    data = []
    for user in pagination.items:
        print(user.to_dict())
        user_dict = user.to_dict()

        if user.locationId:
            location = Location.query.get(user.locationId)
            user_dict["location"] = f"{location.address} - {location.city} - {location.state} - {location.country}" if location else "Unknown"
        else:
            user_dict["location"] = "Unknown"
        data.append(user_dict)

    return jsonify({
        "query": kw,
        "page": page,
        "size": size,
        "total": pagination.total,
        "pages": pagination.pages,
        "count": len(data),
        "results": data,
    })

@users_bp.route('/api/users/<int:userid>', methods=['GET'])
def get_user_detail(userid):
    user = User.query.get(userid)

@users_bp.route('/users/<int:userid>', methods=['GET'])
def user_detail_page(userid):
    user = User.query.filter(User.userId == userid).first()

    user_full_name = ""
    return render_template("demo_user.html", title_name=user_full_name)
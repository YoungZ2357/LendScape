from flask import Blueprint, request, jsonify, render_template
from app import db
from app.users import users_bp
from app.models import User, Location
from decimal import Decimal

@users_bp.route('/page/users/search', methods=['GET'])
def search_page():
    return render_template("demo_user.html")

@users_bp.route('/api/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 20, type=int)

    kw = request.args.get("search", "", type=str)

    query = User.query
    if kw:
        query = query.filter(
            db.or_(
                User.firstName.like(f"%{kw}%"),
                User.lastName.like(f"%{kw}%"),
                User.email.like(f"%{kw}%")
            )
        )

    pagination = query.paginate(page, size, False)

    data = []
    for user in pagination.items:
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


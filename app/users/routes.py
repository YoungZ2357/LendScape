from flask import Blueprint, request, jsonify, render_template
from app import db
from app.users import users_bp
from sqlalchemy import or_
from app.models import User, Location, Order
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
def get_user_stats(userid: int):
    """

    :param userid:
    :return:
    """
    user = User.query.get_or_404(userid)

    borrower_orders = Order.query.filter_by(borrowerId=userid).all()
    lender_orders = Order.query.filter_by(lenderId=userid).all()


    return jsonify({
        'user_info': {
            'userid': user.userid,
            'username': user.username,
            'email': user.email
        },
        'order_statistics': {
            'borrower_count': len(borrower_orders),
            'lender_count': len(lender_orders),
            'total_count': len(borrower_orders) + len(lender_orders)
        },
        'borrower_orders': build_order_info(borrower_orders),
        'lender_orders': build_order_info(lender_orders)
    })


def build_order_info(orders):
    return [{
        'order_id': order.orderId,
        'item_name': order.item.itemName,
        'item_description': order.item.description,
        'item_status': order.item.is_available,
        'created_at': order.created_at.isoformat() if hasattr(order, 'created_at') else None
    } for order in orders]



@users_bp.route('/users/<int:userid>', methods=['GET'])
def user_detail_page(userid):
    """Caution: This page render route contains data query!

    :param userid:
    :return:
    """
    user = User.query.filter(User.userId == userid).first()

    user_full_name = f"{user.firstName}-{user.lastName}"
    user_entity = user.to_dict()
    return render_template("demo_user_detail.html", title_name=user_full_name, user_entity=user_entity)



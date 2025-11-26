from flask import Blueprint, request, jsonify, render_template, session
from app import db
from app.users import users_bp
from sqlalchemy import or_, func
from app.models import User, Location, Order, Item, Review

from app.auth.routes import login_required

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
    user = User.query.filter(User.userId==userid).first()

    borrower_orders = Order.query.filter(Order.borrowerId == userid).all()
    lender_orders = Order.query.filter(Order.renterId == userid).all()


    return jsonify({
        'user_info': {
            'userid': user.userId,
            'username': f"{user.firstName} {user.lastName}",
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
    # print(orders[0].orderId, "\n", orders[1].orderId, "\n", orders[2].orderId)
    query = Item.query
    new_orders = []
    for order in orders:
        target = query.filter(Item.itemId == order.itemId).first()
        order.itemName = target.itemName
        order.description = target.description
        new_orders.append(order)
    return [{
        'order_id': order.orderId,
        'item_name': order.itemName,
        'description': order.description,
        # 'item_status': order.item.is_available,
        'created_at': order.created_at.isoformat() if hasattr(order, 'created_at') else None
    } for order in new_orders]


@users_bp.route('/users/<int:userid>', methods=['GET'])
def user_detail_page(userid):
    """Caution: This page render route contains data query!

    :param userid:
    :return:
    """

    if "user_id" in session and userid is None:
        userid = session['user_id']
    user = User.query.filter(User.userId == userid).first()

    user_full_name = f"{user.firstName}-{user.lastName}"
    user_entity = user.to_dict()
    return render_template("demo_user_detail.html", title_name=user_full_name, user_entity=user_entity, user_id=userid)


@users_bp.route('/api/users/current', methods=['GET'])
@login_required  # 需要导入 from flask_login import login_required, current_user
def get_current_user():
    """
    获取当前登录用户的信息
    """
    try:
        # 从 session 获取用户 ID
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401

        user_id = session['user_id']
        user = User.query.filter_by(userId=user_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_dict = user.to_dict()
        user_dict['locationId'] = user.locationId

        if user.locationId:
            location = Location.query.get(user.locationId)
            user_dict['location'] = location.to_dict() if location else None

        return jsonify(user_dict), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@users_bp.route('/api/users/rating/<int:userid>', methods=['GET'])
@login_required
def calc_rating(userid):

    try:
        avg_rating = (
            db.session.query(func.avg(Review.rating))
            .join(Order, Review.orderId == Order.orderId)
            .filter(Order.renterId == userid)
            .scalar()
        )

        review_count = (
            db.session.query(func.count(Review.reviewId))
            .join(Order, Review.orderId == Order.orderId)
            .filter(Order.renterId == userid)
            .scalar()
        )

        return jsonify({
            'averageRating': float(avg_rating) if avg_rating is not None else None,
            'reviewCount': review_count or 0,
            'userId': userid,
            'ratingType': 'as_renter'
        })

    except Exception as e:
        print(f"Error calculating rating for user {userid}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
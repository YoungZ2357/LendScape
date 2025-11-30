# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ProjectName: LendScape
# FileName: routes.py
# Date: 2025/11/28 11:04
# -------------------------------------------------------------------------
from flask import request, jsonify, session
from app.order import orders_bp
from app.models import User, Item, UserItem, Order, Request
from app import db
from app.auth.routes import login_required
from datetime import datetime
from sqlalchemy import or_, and_


@orders_bp.route("/api/orders/<int:order_id>", methods=["GET"])
@login_required
def get_order_detail(order_id):

    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        current_user_id = session.get('user_id')
        if current_user_id not in [order.renterId, order.borrowerId]:
            return jsonify({'error': 'Forbidden'}), 403

        result = order.to_dict()

        item = Item.query.get(order.itemId)
        if item:
            result['item'] = {
                'itemId': item.itemId,
                'itemName': item.itemName,
                'description': item.description,
                'price': item.price
            }

        renter = User.query.get(order.renterId)
        borrower = User.query.get(order.borrowerId)

        if renter:
            result['renter'] = {
                'userId': renter.userId,
                'username': f"{renter.firstName} {renter.lastName}",
                'email': renter.email
            }

        if borrower:
            result['borrower'] = {
                'userId': borrower.userId,
                'username': f"{borrower.firstName} {borrower.lastName}",
                'email': borrower.email
            }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route("/api/orders", methods=["GET"])
@login_required
def get_orders_list():
    try:

        user_id = request.args.get('user_id', type=int)
        item_id = request.args.get('itemId', type=int)
        status = request.args.get('status')
        role = request.args.get('role')
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)

        # 构建查询
        query = Order.query

        if user_id:
            if role == 'borrower':
                query = query.filter_by(borrowerId=user_id)
            elif role == 'lender':
                query = query.filter_by(renterId=user_id)
            else:
                query = query.filter(
                    or_(Order.borrowerId == user_id,
                        Order.renterId == user_id)
                )

        if item_id:
            query = query.filter_by(itemId=item_id)

        if status:
            query = query.filter_by(status=status)
        query = query.order_by(Order.createdAt.desc())
        paginated = query.paginate(page=page, per_page=size, error_out=False)

        orders = []
        for order in paginated.items:
            order_dict = order.to_dict()
            item = Item.query.get(order.itemId)
            if item:
                order_dict['item_name'] = item.itemName
                order_dict['item_description'] = item.description
                order_dict['item_status'] = item.is_available

            orders.append(order_dict)

        return jsonify({
            'orders': orders,
            'total': paginated.total,
            'page': page,
            'pages': paginated.pages,
            'size': size
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route("/api/orders/user/<int:user_id>", methods=["GET"])
@login_required
def get_user_orders(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        borrower_orders = Order.query.filter_by(borrowerId=user_id).all()
        lender_orders = Order.query.filter_by(renterId=user_id).all()

        return jsonify({
            'borrower_orders': [order.to_dict() for order in borrower_orders],
            'lender_orders': [order.to_dict() for order in lender_orders],
            'total_borrower': len(borrower_orders),
            'total_lender': len(lender_orders)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route("/api/orders/borrower/<int:user_id>", methods=["GET"])
@login_required
def get_borrower_orders(user_id):
    try:
        orders = Order.query.filter_by(borrowerId=user_id).order_by(Order.createdAt.desc()).all()

        result = []
        for order in orders:
            order_dict = order.to_dict()
            item = Item.query.get(order.itemId)
            if item:
                order_dict['item_name'] = item.itemName
                order_dict['item_description'] = item.description
                order_dict['item_status'] = item.is_available
            renter = User.query.get(order.renterId)
            if renter:
                order_dict['renter_name'] = f"{renter.firstName} {renter.lastName}"

            result.append(order_dict)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route("/api/orders/lender/<int:user_id>", methods=["GET"])
@login_required
def get_lender_orders(user_id):
    try:
        orders = Order.query.filter_by(renterId=user_id).order_by(Order.createdAt.desc()).all()

        result = []
        for order in orders:
            order_dict = order.to_dict()
            item = Item.query.get(order.itemId)
            if item:
                order_dict['item_name'] = item.itemName
                order_dict['item_description'] = item.description
                order_dict['item_status'] = item.is_available
            borrower = User.query.get(order.borrowerId)
            if borrower:
                order_dict['borrower_name'] = f"{borrower.firstName} {borrower.lastName}"

            result.append(order_dict)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route("/api/orders/<int:order_id>/status", methods=["PUT"])
@login_required
def update_order_status(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        current_user_id = session.get('user_id')
        if current_user_id != order.renterId:
            return jsonify({'error': 'Only the renter can update order status'}), 403

        data = request.get_json()
        new_status = data.get('status')

        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        valid_transitions = {
            'pending': ['active', 'cancelled'],
            'active': ['complete', 'cancelled'],
            'complete': [],
            'cancelled': []
        }

        current_status = order.status
        if new_status not in valid_transitions.get(current_status, []):
            return jsonify({
                'error': f'Invalid status transition from {current_status} to {new_status}'
            }), 400

        order.status = new_status
        order.updatedAt = datetime.utcnow()

        if new_status in ['complete', 'cancelled']:
            item = Item.query.get(order.itemId)
            if item:
                item.is_available = True

        db.session.commit()

        return jsonify({
            'orderId': order.orderId,
            'status': order.status,
            'message': f'Order status updated to {new_status}'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orders_bp.route("/api/orders/<int:order_id>/complete", methods=["PUT"])
@login_required
def complete_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        current_user_id = session.get('user_id')
        if current_user_id not in [order.renterId, order.borrowerId]:
            return jsonify({'error': 'Forbidden'}), 403

        if order.status != 'active':
            return jsonify({'error': 'Only active orders can be completed'}), 400

        order.status = 'complete'
        order.completedAt = datetime.utcnow()
        order.updatedAt = datetime.utcnow()

        item = Item.query.get(order.itemId)
        if item:
            item.is_available = True

        db.session.commit()

        return jsonify({
            'orderId': order.orderId,
            'status': order.status,
            'completedAt': order.completedAt.isoformat() if order.completedAt else None,
            'message': 'Order completed successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orders_bp.route("/api/orders/<int:order_id>/cancel", methods=["PUT"])
@login_required
def cancel_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        current_user_id = session.get('user_id')
        if current_user_id not in [order.renterId, order.borrowerId]:
            return jsonify({'error': 'Forbidden'}), 403

        if order.status in ['complete', 'cancelled']:
            return jsonify({'error': f'Cannot cancel {order.status} order'}), 400

        order.status = 'cancelled'
        order.updatedAt = datetime.utcnow()

        item = Item.query.get(order.itemId)
        if item:
            item.is_available = True

        associated_request = Request.query.filter_by(orderId=order.orderId).first()
        if associated_request:
            associated_request.status = 'CANCELLED'
            associated_request.updatedAt = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'orderId': order.orderId,
            'status': order.status,
            'message': 'Order cancelled successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orders_bp.route("/api/orders/<int:order_id>", methods=["DELETE"])
@login_required
def delete_order(order_id):
    try:
        current_user_id = session.get('user_id')
        user = User.query.get(current_user_id)

        if not user or user.userClass.value != 'admin':
            return jsonify({'error': 'Admin permission required'}), 403

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        Request.query.filter_by(orderId=order_id).update({'orderId': None})

        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': 'Order deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orders_bp.route("/api/orders/item/<int:item_id>", methods=["GET"])
@login_required
def get_relating_order(item_id):
    print("/api/order/item triggered")
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        status = request.args.get('status')

        query = Order.query.filter_by(itemId=item_id)

        if status:
            query = query.filter_by(status=status)

        query = query.order_by(Order.createdAt.desc())

        paginated = query.paginate(page=page, per_page=size, error_out=False)

        orders = []
        for order in paginated.items:
            order_dict = order.to_dict()
            print(order_dict)

            renter = User.query.get(order.renterId)
            if renter:
                order_dict['renter'] = {
                    'userId': renter.userId,
                    'username': f"{renter.firstName} {renter.lastName}",
                    'email': renter.email
                }

            borrower = User.query.get(order.borrowerId)
            if borrower:
                order_dict['borrower'] = {
                    'userId': borrower.userId,
                    'username': f"{borrower.firstName} {borrower.lastName}",
                    'email': borrower.email
                }

            order_dict['item'] = {
                'itemId': item.itemId,
                'itemName': item.itemName,
                'description': item.description,
                'price': item.price,
                'is_available': item.is_available
            }

            related_request = Request.query.filter_by(orderId=order.orderId).first()
            if related_request:
                order_dict['request'] = {
                    'requestId': related_request.requestId,
                    'status': related_request.status.value if related_request.status else None,
                    'startDate': related_request.startDate.isoformat() if related_request.startDate else None,
                    'endDate': related_request.endDate.isoformat() if related_request.endDate else None
                }

            orders.append(order_dict)
        print({
            'itemId': item_id,
            'itemName': item.itemName,
            'orders': orders,
            'total': paginated.total,
            'page': page,
            'pages': paginated.pages,
            'size': size,
            'summary': {
                'total_orders': paginated.total,
                'pending': Order.query.filter_by(itemId=item_id, status='pending').count(),
                'active': Order.query.filter_by(itemId=item_id, status='active').count(),
                'complete': Order.query.filter_by(itemId=item_id, status='complete').count(),
                'cancelled': Order.query.filter_by(itemId=item_id, status='cancelled').count()
            }
        })
        return jsonify({
            'itemId': item_id,
            'itemName': item.itemName,
            'orders': orders,
            'total': paginated.total,
            'page': page,
            'pages': paginated.pages,
            'size': size,
            'summary': {
                'total_orders': paginated.total,
                'pending': Order.query.filter_by(itemId=item_id, status='pending').count(),
                'active': Order.query.filter_by(itemId=item_id, status='active').count(),
                'complete': Order.query.filter_by(itemId=item_id, status='complete').count(),
                'cancelled': Order.query.filter_by(itemId=item_id, status='cancelled').count()
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

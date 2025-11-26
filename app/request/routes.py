# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ProjectName: LendScape
# FileName: routes.py
# Date: 2025/11/26 18:27
# -------------------------------------------------------------------------
from flask import request, jsonify, render_template, session
from app.request import requests_bp
from app.models import User, Item, Request, Order, RequestStatus
from app import db
from app.auth.routes import login_required
from datetime import datetime


@requests_bp.route("/api/requests/<int:user_id>", methods=["GET"])
@login_required
def get_requests(user_id):
    try:

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        sent_requests = Request.query.filter_by(requesterId=user_id).all()

        received_requests = Request.query.filter_by(ownerId=user_id).all()

        return jsonify({
            'sent': [req.to_dict() for req in sent_requests],
            'received': [req.to_dict() for req in received_requests],
            'total_sent': len(sent_requests),
            'total_received': len(received_requests)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@requests_bp.route("/api/requests/<int:request_id>", methods=["GET"])
@login_required
def get_request_detail(request_id):
    try:
        req = Request.query.get(request_id)
        if not req:
            return jsonify({'error': 'Request not found'}), 404

        current_user_id = session.get('user_id')
        if current_user_id not in [req.requesterId, req.ownerId]:
            user = User.query.get(current_user_id)
            if not user or user.userClass.value != 'admin':
                return jsonify({'error': 'Forbidden'}), 403

        return jsonify(req.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@requests_bp.route("/api/requests", methods=["POST"])
@login_required
def make_request():
    try:
        data = request.get_json()

        required_fields = ['itemId', 'startDate', 'endDate']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        current_user_id = session.get('user_id')


        item = Item.query.get(data['itemId'])
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        if item.userId == current_user_id:
            return jsonify({'error': 'Cannot request your own item'}), 400

        if not item.is_available:
            return jsonify({'error': 'Item is not available'}), 409

        try:
            start_date = datetime.fromisoformat(data['startDate'])
            end_date = datetime.fromisoformat(data['endDate'])
        except:
            return jsonify({'error': 'Invalid date format'}), 400

        if start_date >= end_date:
            return jsonify({'error': 'End date must be after start date'}), 400
        if start_date < datetime.now():
            return jsonify({'error': 'Start date cannot be in the past'}), 400

        new_request = Request(
            requesterId=current_user_id,
            ownerId=item.userId,
            itemId=item.itemId,
            startDate=start_date,
            endDate=end_date,
            message=data.get('message', ''),
            status=RequestStatus.PENDING
        )

        db.session.add(new_request)
        db.session.commit()

        return jsonify(new_request.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@requests_bp.route("/api/requests/<int:request_id>", methods=["PUT"])
@login_required
def update_request(request_id):
    try:
        req = Request.query.get(request_id)
        if not req:
            return jsonify({'error': 'Request not found'}), 404

        current_user_id = session.get('user_id')
        if req.requesterId != current_user_id:
            return jsonify({'error': 'Forbidden'}), 403

        if req.status != RequestStatus.PENDING:
            return jsonify({'error': 'Can only update pending requests'}), 409

        data = request.get_json()

        if 'message' in data:
            req.message = data['message']

        if 'startDate' in data:
            try:
                req.startDate = datetime.fromisoformat(data['startDate'])
            except:
                return jsonify({'error': 'Invalid start date format'}), 400

        if 'endDate' in data:
            try:
                req.endDate = datetime.fromisoformat(data['endDate'])
            except:
                return jsonify({'error': 'Invalid end date format'}), 400

        if req.startDate >= req.endDate:
            return jsonify({'error': 'End date must be after start date'}), 400

        req.updatedAt = datetime.utcnow()
        db.session.commit()

        return jsonify(req.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@requests_bp.route("/api/requests/<int:request_id>", methods=["DELETE"])
@login_required
def delete_request(request_id):
    try:
        req = Request.query.get(request_id)
        if not req:
            return jsonify({'error': 'Request not found'}), 404

        current_user_id = session.get('user_id')
        if req.requesterId != current_user_id:
            return jsonify({'error': 'Forbidden'}), 403

        if req.status != RequestStatus.PENDING:
            return jsonify({'error': 'Can only delete pending requests'}), 409

        req.status = RequestStatus.CANCELLED
        req.updatedAt = datetime.utcnow()
        db.session.commit()

        return jsonify({'message': 'Request cancelled successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@requests_bp.route("/api/requests/<int:request_id>/accept", methods=["PUT"])
@login_required
def accept_request(request_id):

    try:
        req = Request.query.get(request_id)
        if not req:
            return jsonify({'error': 'Request not found'}), 404


        current_user_id = session.get('user_id')
        if req.ownerId != current_user_id:
            return jsonify({'error': 'Forbidden'}), 403

        if req.status != RequestStatus.PENDING:
            return jsonify({'error': 'Request is not pending'}), 409

        item = Item.query.get(req.itemId)
        if not item or not item.is_available:
            return jsonify({'error': 'Item is no longer available'}), 409

        # 创建订单
        new_order = Order(
            renterId=req.ownerId,
            borrowerId=req.requesterId,
            itemId=req.itemId,
            status='pending'
        )
        db.session.add(new_order)
        db.session.flush()


        req.status = RequestStatus.ACCEPTED
        req.orderId = new_order.orderId
        req.updatedAt = datetime.utcnow()

        item.is_available = False

        db.session.commit()

        return jsonify({
            'requestId': req.requestId,
            'status': req.status.value,
            'orderId': new_order.orderId,
            'message': 'Request accepted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@requests_bp.route("/api/requests/<int:request_id>/decline", methods=["PUT"])
@login_required
def decline_request(request_id):
    return reject_request(request_id)


@requests_bp.route("/api/requests/<int:request_id>/reject", methods=["PUT"])
@login_required
def reject_request(request_id):
    try:
        req = Request.query.get(request_id)
        if not req:
            return jsonify({'error': 'Request not found'}), 404

        current_user_id = session.get('user_id')
        if req.ownerId != current_user_id:
            return jsonify({'error': 'Forbidden'}), 403

        if req.status != RequestStatus.PENDING:
            return jsonify({'error': 'Request is not pending'}), 409

        data = request.get_json() or {}
        reason = data.get('reason', '')

        req.status = RequestStatus.REJECTED
        req.rejectionReason = reason
        req.updatedAt = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'requestId': req.requestId,
            'status': req.status.value,
            'rejectionReason': req.rejectionReason,
            'message': 'Request rejected successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
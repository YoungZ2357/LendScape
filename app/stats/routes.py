# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ProjectName: LendScape
# FileName: routes.py
# Date: 2025/12/2 11:31
# -------------------------------------------------------------------------
from flask import request, jsonify, session, render_template
from app.models import *
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func, case, desc, extract, and_
from app.stats import stats_bp


@stats_bp.route('/api/stats/user/average-rental-times', methods=['GET'])
def get_user_average_rental_times():
    """
    获取用户平均的借入时间、借出时间
    借入时间：borrower作为borrowerId的订单持续时间
    借出时间：renter作为renterId的订单持续时间
    """
    try:
        # 获取所有已完成订单
        completed_orders = Order.query.filter(
            Order.status == StatusType.complete
        ).all()

        if not completed_orders:
            return jsonify({
                'success': True,
                'message': 'No orders',
                'data': {
                    'average_borrow_time': 0,
                    'average_lend_time': 0,
                    'total_orders': 0
                }
            })

        borrow_stats = db.session.query(
            func.avg(
                extract('epoch', Request.endDate - Request.startDate) / 86400.0  # 转换为天数
            ).label('avg_borrow_days')
        ).join(
            Order, Order.requestId == Request.requestId
        ).filter(
            Order.status == StatusType.complete
        ).first()

        lend_stats = db.session.query(
            func.avg(
                extract('epoch', Request.endDate - Request.startDate) / 86400.0  # 转换为天数
            ).label('avg_lend_days')
        ).join(
            Order, Order.requestId == Request.requestId
        ).join(
            Item, Item.itemId == Request.itemId
        ).filter(
            Order.status == StatusType.complete
        ).first()

        avg_borrow_days = round(float(borrow_stats[0]) if borrow_stats[0] else 0, 2)
        avg_lend_days = round(float(lend_stats[0]) if lend_stats[0] else 0, 2)

        return jsonify({
            'success': True,
            'message': 'Avg rent days',
            'data': {
                'average_borrow_days': avg_borrow_days,
                'average_lend_days': avg_lend_days,
                'unit': 'days'
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to fetch avg rental time: {str(e)}'
        }), 500


@stats_bp.route('/api/stats/user/activity-last-three-months/<int:user_id>', methods=['GET'])
def get_user_activity_last_three_months(user_id):
    """
    获取用户既往三月的活跃度（借入+借出请求）
    统计最近三个月内用户作为requester和owner的request总数
    """
    try:
        three_months_ago = datetime.now() - timedelta(days=90)

        borrow_requests = Request.query.filter(
            Request.requesterId == user_id,
            Request.createdAt >= three_months_ago
        ).count()

        lend_requests = Request.query.filter(
            Request.ownerId == user_id,
            Request.createdAt >= three_months_ago
        ).count()

        total_activity = borrow_requests + lend_requests

        return jsonify({
            'success': True,
            'message': 'User activity',
            'data': {
                'user_id': user_id,
                'borrow_requests': borrow_requests,
                'lend_requests': lend_requests,
                'total_activity': total_activity,
                'period': 'last_three_months',
                'period_start': three_months_ago.strftime('%Y-%m-%d')
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to fetch user activity: {str(e)}'
        }), 500


@stats_bp.route('/api/stats/top-active-users', methods=['GET'])
def get_top_active_users():
    """
    获取活跃用户列表
    活跃度 = 用户request数 * 0.2 + 用户order数 * 0.8

    """
    try:

        limit = request.args.get('limit', type=int)
        min_score = request.args.get('min_score', type=float)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)

        per_page = min(per_page, 500)

        user_request_counts = db.session.query(
            Request.requesterId.label('user_id'),
            func.count(Request.requestId).label('request_count')
        ).group_by(Request.requesterId).subquery()

        borrower_order_counts = db.session.query(
            Order.borrowerId.label('user_id'),
            func.count(Order.orderId).label('order_count')
        ).group_by(Order.borrowerId).subquery()

        renter_order_counts = db.session.query(
            Order.renterId.label('user_id'),
            func.count(Order.orderId).label('order_count')
        ).group_by(Order.renterId).subquery()

        query = db.session.query(
            User.userId,
            User.firstName,
            User.lastName,
            User.email,
            User.locationId,
            func.coalesce(user_request_counts.c.request_count, 0).label('request_count'),
            func.coalesce(borrower_order_counts.c.order_count, 0).label('borrower_count'),
            func.coalesce(renter_order_counts.c.order_count, 0).label('renter_count'),
            (
                    func.coalesce(borrower_order_counts.c.order_count, 0) +
                    func.coalesce(renter_order_counts.c.order_count, 0)
            ).label('total_orders'),
            (
                    func.coalesce(user_request_counts.c.request_count, 0) * 0.2 +
                    (
                            func.coalesce(borrower_order_counts.c.order_count, 0) +
                            func.coalesce(renter_order_counts.c.order_count, 0)
                    ) * 0.8
            ).label('activity_score')
        ).outerjoin(
            user_request_counts, User.userId == user_request_counts.c.user_id
        ).outerjoin(
            borrower_order_counts, User.userId == borrower_order_counts.c.user_id
        ).outerjoin(
            renter_order_counts, User.userId == renter_order_counts.c.user_id
        )

        if min_score is not None:
            query = query.having(
                (
                        func.coalesce(user_request_counts.c.request_count, 0) * 0.2 +
                        (
                                func.coalesce(borrower_order_counts.c.order_count, 0) +
                                func.coalesce(renter_order_counts.c.order_count, 0)
                        ) * 0.8
                ) >= min_score
            )

        query = query.order_by(desc('activity_score'))

        total_users = query.count()

        if limit is not None and limit > 0:
            active_users = query.limit(limit).all()
        else:
            offset = (page - 1) * per_page
            active_users = query.offset(offset).limit(per_page).all()

        result = []
        for idx, user in enumerate(active_users, start=1 if limit else (page - 1) * per_page + 1):
            user_data = {
                'rank': idx,
                'user_id': user.userId,
                'first_name': user.firstName,
                'last_name': user.lastName,
                'email': user.email,
                'request_count': user.request_count,
                'borrower_count': user.borrower_count,
                'renter_count': user.renter_count,
                'total_orders': user.total_orders,
                'activity_score': round(float(user.activity_score), 2)
            }

            if user.locationId:
                location = Location.query.get(user.locationId)
                if location:
                    user_data['location'] = {
                        'city': location.city,
                        'state': location.state,
                        'country': location.country,
                        'full_address': f"{location.city}, {location.state}, {location.country}"
                    }
                else:
                    user_data['location'] = None
            else:
                user_data['location'] = None

            result.append(user_data)

        response_data = {
            'success': True,
            'message': 'Fetched active users',
            'data': result,
            'count': len(result)
        }

        if limit is None or limit <= 0:
            response_data['pagination'] = {
                'page': page,
                'per_page': per_page,
                'total_users': total_users,
                'total_pages': (total_users + per_page - 1) // per_page if per_page > 0 else 1,
                'has_next': page * per_page < total_users,
                'has_prev': page > 1
            }
        else:
            response_data['limit'] = limit
            response_data['total_available'] = total_users

        return jsonify(response_data)

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取数据失败: {str(e)}'
        }), 500


@stats_bp.route('/top-active-locations', methods=['GET'])
def get_top_active_locations():
    """
    获取Top5 活跃地区
    地区活跃度 = 总request数 * 0.2 + 总order数 * 0.8
    通过User的locationId关联Location表
    """
    try:
        location_request_counts = db.session.query(
            User.locationId,
            func.count(Request.requestId).label('request_count')
        ).join(
            Request, User.userId == Request.requesterId
        ).group_by(User.locationId).subquery()

        location_order_counts = db.session.query(
            User.locationId,
            func.count(Order.orderId).label('order_count')
        ).join(
            Order, User.userId == Order.borrowerId
        ).group_by(User.locationId).union_all(
            db.session.query(
                User.locationId,
                func.count(Order.orderId).label('order_count')
            ).join(
                Order, User.userId == Order.renterId
            ).group_by(User.locationId)
        ).subquery()

        total_order_counts = db.session.query(
            location_order_counts.c.locationId,
            func.sum(location_order_counts.c.order_count).label('total_orders')
        ).group_by(location_order_counts.c.locationId).subquery()

        active_locations = db.session.query(
            Location.locationId,
            Location.city,
            Location.state,
            Location.country,
            func.coalesce(location_request_counts.c.request_count, 0).label('request_count'),
            func.coalesce(total_order_counts.c.total_orders, 0).label('order_count'),
            (
                    func.coalesce(location_request_counts.c.request_count, 0) * 0.2 +
                    func.coalesce(total_order_counts.c.total_orders, 0) * 0.8
            ).label('activity_score')
        ).outerjoin(
            location_request_counts, Location.locationId == location_request_counts.c.locationId
        ).outerjoin(
            total_order_counts, Location.locationId == total_order_counts.c.locationId
        ).filter(
            Location.locationId.isnot(None)
        ).order_by(
            desc('activity_score')
        ).limit(5).all()

        result = []
        for location in active_locations:
            result.append({
                'location_id': location.locationId,
                'city': location.city,
                'state': location.state,
                'country': location.country,
                'request_count': location.request_count,
                'order_count': location.order_count,
                'activity_score': round(float(location.activity_score), 2)
            })

        return jsonify({
            'success': True,
            'message': 'Fetched top locations',
            'data': result,
            'count': len(result)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取数据失败: {str(e)}'
        }), 500


@stats_bp.route('/api/stats/user/lending-success-rate/<int:user_id>', methods=['GET'])
def get_user_lending_success_rate(user_id):
    """
    获取用户成功借出率
    成功率 = request接受数 / (request接受数 + request拒绝数) * 100%
    """
    try:
        request_stats = db.session.query(
            Request.status,
            func.count(Request.requestId).label('count')
        ).filter(
            Request.ownerId == user_id
        ).group_by(Request.status).all()

        accepted_count = 0
        rejected_count = 0
        total_processed = 0

        for status, count in request_stats:
            if status == RequestStatus.ACCEPTED:
                accepted_count = count
                total_processed += count
            elif status == RequestStatus.REJECTED:
                rejected_count = count
                total_processed += count

        if total_processed > 0:
            success_rate = (accepted_count / total_processed) * 100
        else:
            success_rate = 0

        return jsonify({
            'success': True,
            'message': 'success rate',
            'data': {
                'user_id': user_id,
                'accepted_requests': accepted_count,
                'rejected_requests': rejected_count,
                'total_processed_requests': total_processed,
                'success_rate': round(success_rate, 2),
                'success_rate_unit': 'percentage'
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取数据失败: {str(e)}'
        }), 500


@stats_bp.route('/stats/top-users', methods=['GET'])
def top_users_page():
    return render_template("top_users.html")
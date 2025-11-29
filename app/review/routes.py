# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ProjectName: LendScape
# FileName: routes.py
# Date: 2025/11/28 16:11
# -------------------------------------------------------------------------
from app.review import reviews_bp
from flask import request, jsonify, session
from app.models import Order, Review, User, Item, db
from app.auth.routes import login_required
from datetime import datetime


@reviews_bp.route('/api/reviews/<int:order_id>', methods=['POST'])
@login_required
def make_review(order_id):
    """
    创建新的评论
    只有借用者（borrower）可以对订单进行评论
    """
    try:

        current_user_id = session.get('user_id')

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        if order.borrowerId != current_user_id:
            return jsonify({'error': 'Only borrowers can write reviews'}), 403

        existing_review = Review.query.filter_by(orderId=order_id).first()
        if existing_review:
            return jsonify({'error': 'Review already exists for this order'}), 409

        data = request.get_json()
        rating = data.get('rating')
        content = data.get('content', '')
        item_id = data.get('itemId', order.itemId)

        if rating is None:
            return jsonify({'error': 'Rating is required'}), 400

        try:
            rating = float(rating)
            if rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid rating value'}), 400

        new_review = Review(
            userId=current_user_id,
            itemId=item_id,
            orderId=order_id,
            content=content,
            rating=rating
        )

        db.session.add(new_review)

        order.reviewId = new_review.reviewId

        db.session.commit()

        return jsonify({
            'message': 'Review created successfully',
            'review': new_review.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@reviews_bp.route('/api/reviews/order/<int:order_id>', methods=['GET'])
@login_required
def get_order_review(order_id):
    """
    获取特定订单的评论
    """
    try:
        # 获取订单
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # 获取评论
        review = Review.query.filter_by(orderId=order_id).first()

        if review:
            review_dict = review.to_dict()

            # 添加评论者信息
            reviewer = User.query.get(review.userId)
            if reviewer:
                review_dict['reviewer'] = {
                    'userId': reviewer.userId,
                    'firstName': reviewer.firstName,
                    'lastName': reviewer.lastName,
                    'email': reviewer.email
                }

            return jsonify(review_dict), 200
        else:
            return jsonify(None), 204  # No Content

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reviews_bp.route('/api/reviews/<int:review_id>', methods=['PUT'])
@login_required
def update_review(review_id):
    try:
        current_user_id = session.get('user_id')

        review = Review.query.get(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404

        if review.userId != current_user_id:
            return jsonify({'error': 'You can only edit your own reviews'}), 403

        # 获取更新数据
        data = request.get_json()

        if 'rating' in data:
            rating = data['rating']
            try:
                rating = float(rating)
                if rating < 1 or rating > 5:
                    return jsonify({'error': 'Rating must be between 1 and 5'}), 400
                review.rating = rating
            except (TypeError, ValueError):
                return jsonify({'error': 'Invalid rating value'}), 400

        if 'content' in data:
            review.content = data['content']

        db.session.commit()

        return jsonify({
            'message': 'Review updated successfully',
            'review': review.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@reviews_bp.route('/api/reviews/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    try:
        current_user_id = session.get('user_id')
        current_user = User.query.get(current_user_id)

        review = Review.query.get(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404


        is_admin = current_user.userClass and current_user.userClass.value == 'admin'
        if review.userId != current_user_id and not is_admin:
            return jsonify({'error': 'You can only delete your own reviews'}), 403

        order = Order.query.filter_by(reviewId=review_id).first()
        if order:
            order.reviewId = None

        db.session.delete(review)
        db.session.commit()

        return jsonify({'message': 'Review deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@reviews_bp.route('/api/reviews/item/<int:item_id>', methods=['GET'])
def get_item_reviews(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # 获取评论
        reviews_query = Review.query.filter_by(itemId=item_id)

        # 排序（最新的在前）
        # reviews_query = reviews_query.order_by(Review.createdAt.desc()) if hasattr(Review, 'createdAt') else reviews_query

        # 分页
        pagination = reviews_query.paginate(page=page, per_page=per_page, error_out=False)

        reviews = []
        for review in pagination.items:
            review_dict = review.to_dict()

            # 添加评论者信息
            reviewer = User.query.get(review.userId)
            if reviewer:
                review_dict['reviewer'] = {
                    'userId': reviewer.userId,
                    'firstName': reviewer.firstName,
                    'lastName': reviewer.lastName,
                    'fullName': f"{reviewer.firstName} {reviewer.lastName}"
                }

            reviews.append(review_dict)

        # 计算统计信息
        all_reviews = Review.query.filter_by(itemId=item_id).all()
        if all_reviews:
            ratings = [float(r.rating) for r in all_reviews if r.rating]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            rating_distribution = {
                '5': len([r for r in ratings if r >= 4.5]),
                '4': len([r for r in ratings if 3.5 <= r < 4.5]),
                '3': len([r for r in ratings if 2.5 <= r < 3.5]),
                '2': len([r for r in ratings if 1.5 <= r < 2.5]),
                '1': len([r for r in ratings if r < 1.5])
            }
        else:
            avg_rating = 0
            rating_distribution = {'5': 0, '4': 0, '3': 0, '2': 0, '1': 0}

        return jsonify({
            'reviews': reviews,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'statistics': {
                'average_rating': round(avg_rating, 2),
                'total_reviews': len(all_reviews),
                'rating_distribution': rating_distribution
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ProjectName: LendScape
# FileName: routes.py
# Date: 2025/11/19 13:34
# -------------------------------------------------------------------------
from flask import Blueprint, render_template, jsonify, session, request
from app import db
from app.auth.routes import login_required
from app.locations import locations_bp
from app.models import Location, User

from flask import session


@locations_bp.route('/api/locations/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    """更新用户地址"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401

        current_user_id = session['user_id']

        data = request.get_json()

        # 验证必填字段
        required_fields = ['street', 'city', 'state', 'zip']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # 查找地址
        location = Location.query.filter_by(locationId=location_id).first()
        if not location:
            return jsonify({'error': 'Location not found'}), 404

        # 验证权限 - 使用 session 中的 user_id
        user = User.query.filter_by(
            userId=current_user_id,
            locationId=location_id
        ).first()

        if not user:
            return jsonify({'error': 'Unauthorized to update this location'}), 403

        # 更新地址
        location.address = data.get('street')
        location.city = data.get('city')
        location.state = data.get('state')
        location.postcode = data.get('zip')

        if 'country' in data:
            location.country = data.get('country')

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Location updated successfully',
            'location': location.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

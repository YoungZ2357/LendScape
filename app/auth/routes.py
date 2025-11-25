from flask import request, jsonify, session, g, redirect, url_for, render_template
from app.auth import auth_bp
from app import db, supabase_client
from app.models import User, Location, UserStatus, UserClass
from functools import wraps
import hashlib
import hmac
import secrets
from sqlalchemy import text





def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401

        user = User.query.filter_by(userId=session['user_id']).first()
        if not user:
            session.clear()
            return jsonify({'error': 'User not found'}), 401

        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401

        user = User.query.filter_by(userId=session['user_id']).first()
        if not user:
            session.clear()
            return jsonify({'error': 'User not found'}), 401

        if user.userClass != UserClass.ADMIN:
            return jsonify({'error': 'Admin access required'}), 403

        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function

def location_required(f):
    """装饰器：要求用户必须有位置信息"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not g.current_user.locationId:
            return jsonify({
                'error': 'Location required',
                'redirect': '/auth/location'
            }), 302
        return f(*args, **kwargs)
    return decorated_function

# 密码哈希函数（模拟PostgreSQL的hash_password）
def hash_password(password):
    """使用SHA256哈希密码"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    return f"{salt}${pwd_hash}"

def verify_password(password, stored_password):
    """验证密码"""
    try:
        salt, pwd_hash = stored_password.split('$')
        test_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
        return test_hash == pwd_hash
    except:
        return False

@auth_bp.route('/login')
def login_page():
    """渲染登录页面"""
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')

# 添加位置添加页面路由（可选）
@auth_bp.route('/add-location')
@login_required
def add_location_page():

    if g.current_user.locationId:
        return redirect(url_for('main.index'))
    return render_template('auth/add_location.html')




@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    """用户注册"""
    try:
        data = request.get_json()

        # 验证必填字段
        required_fields = ['firstName', 'lastName', 'email', 'phoneNumber', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400

        # 验证密码长度
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400

        # 检查邮箱是否已存在
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400

        # 使用Supabase Auth创建用户
        auth_response = supabase_client.auth.sign_up({
            'email': data['email'],
            'password': data['password'],
            'options': {
                'data': {
                    'first_name': data['firstName'],
                    'last_name': data['lastName'],
                    'phone_number': data['phoneNumber']
                }
            }
        })

        if auth_response.user is None:
            return jsonify({'error': 'Failed to create auth user'}), 500

        # 哈希密码
        hashed_password = hash_password(data['password'])

        # 创建用户记录
        new_user = User(
            auth_id=auth_response.user.id,
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email'],
            phoneNumber=int(data['phoneNumber']),
            pwd=hashed_password,
            userClass=UserClass.ACTIVE,
            status=UserStatus.ACTIVE
        )

        db.session.add(new_user)
        db.session.commit()

        # 设置会话
        session['user_id'] = new_user.userId
        session['auth_id'] = new_user.auth_id

        return jsonify({
            'message': 'User created successfully',
            'user': new_user.to_dict(),
            'requiresLocation': new_user.locationId is None
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/signin', methods=['POST'])
def signin():
    """用户登录"""
    try:
        data = request.get_json()

        # 验证必填字段
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400

        # 使用Supabase Auth登录
        auth_response = supabase_client.auth.sign_in_with_password({
            'email': data['email'],
            'password': data['password']
        })

        if auth_response.user is None:
            return jsonify({'error': 'Invalid email or password'}), 401

        # 获取用户信息
        user = User.query.filter_by(auth_id=auth_response.user.id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # 检查用户状态
        if user.status == UserStatus.BANNED:
            return jsonify({'error': 'Account is banned'}), 403

        if user.status == UserStatus.DEACTIVATED:
            return jsonify({'error': 'Account is deactivated'}), 403

        # 设置会话
        session['user_id'] = user.userId
        session['auth_id'] = user.auth_id

        # 获取位置信息
        location_data = None
        if user.locationId:
            location = Location.query.filter_by(locationId=user.locationId).first()
            if location:
                location_data = location.to_dict()

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'location': location_data,
            'requiresLocation': user.locationId is None
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    """用户登出"""
    try:
        # 使用Supabase Auth登出
        supabase_client.auth.sign_out()

        # 清除会话
        session.clear()

        return jsonify({'message': 'Logout successful'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """获取当前用户信息"""
    try:
        user = g.current_user

        # 获取位置信息
        location_data = None
        if user.locationId:
            location = Location.query.filter_by(locationId=user.locationId).first()
            if location:
                location_data = location.to_dict()

        return jsonify({
            'user': user.to_dict(),
            'location': location_data
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/location', methods=['POST'])
@login_required
def add_location():
    """添加用户位置"""
    try:
        data = request.get_json()
        user = g.current_user

        # 检查用户是否已有位置
        if user.locationId:
            return jsonify({'error': 'User already has a location'}), 400

        # 验证必填字段
        required_fields = ['address', 'city', 'state', 'country', 'postcode']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400

        # 创建位置记录
        new_location = Location(
            address=data['address'],
            city=data['city'],
            state=data['state'],
            country=data['country'],
            postcode=data['postcode'],
            is_default=True
        )

        db.session.add(new_location)
        db.session.flush()  # 获取locationId但不提交

        # 更新用户的locationId
        user.locationId = new_location.locationId
        db.session.commit()

        return jsonify({
            'message': 'Location added successfully',
            'location': new_location.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/location', methods=['PUT'])
@login_required
def update_location():
    """更新用户位置"""
    try:
        data = request.get_json()
        user = g.current_user

        if not user.locationId:
            return jsonify({'error': 'No location to update'}), 404

        location = Location.query.filter_by(locationId=user.locationId).first()
        if not location:
            return jsonify({'error': 'Location not found'}), 404

        # 更新位置信息
        if 'address' in data:
            location.address = data['address']
        if 'city' in data:
            location.city = data['city']
        if 'state' in data:
            location.state = data['state']
        if 'country' in data:
            location.country = data['country']
        if 'postcode' in data:
            location.postcode = data['postcode']

        db.session.commit()

        return jsonify({
            'message': 'Location updated successfully',
            'location': location.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/check-auth', methods=['GET'])
def check_auth():
    """检查认证状态"""
    print("check-auth triggered")
    try:
        if 'user_id' not in session:
            print(session)
            return jsonify({'authenticated': False}), 200

        user = User.query.filter_by(userId=session['userid']).first()
        print(user.to_dict())
        if not user:
            session.clear()
            return jsonify({'authenticated': False}), 200

        # 获取位置信息
        location_data = None
        if user.locationId:
            location = Location.query.filter_by(locationId=user.locationId).first()
            if location:
                location_data = location.to_dict()

        return jsonify({
            'authenticated': True,
            'user': user.to_dict(),
            'location': location_data,
            'requiresLocation': user.locationId is None
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
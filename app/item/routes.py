from flask import request, jsonify, render_template, session
from app.item import items_bp
from app.models import User, Item, UserItem, Order, Review
from app import db
from app.auth.routes import login_required


@items_bp.route("/api/items", methods=['GET'])
def get_items():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 20, type=int)
    print("routes triggered")
    kw = request.args.get("search", "", type=str).strip()

    query = Item.query
    if kw:
        query = query.filter(Item.itemName.like(f"%{kw}%"))

    pagination = query.paginate(
        page=page,
        per_page=size,
        error_out=False
    )
    data = []
    for item in pagination.items:
        item_dict = item.to_dict()

        user = User.query.get(item.userId)
        item_dict['owner_name'] = f"{user.firstName} {user.lastName}" if user else "Unknown"
        data.append(item_dict)
    print(kw)
    return jsonify({
        "query": kw,
        "page": page,
        "size": size,
        "total": pagination.total,
        "pages": pagination.pages,
        "count": len(data),
        "results": data,
    })

@items_bp.route("/items/search")
def search_page():
    return render_template('demo_search.html')





@items_bp.route("/api/items/ownership/<int:userid>")
def show_list_user(userid):
    """
    This route shares the same rendering with user profile rendering
    :param userid:
    :return:
    """

    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 8, type=int)
    query = (Item.query
              .join(UserItem, UserItem.itemid == Item.itemId)
              .filter(UserItem.userid == userid))

    pagination = query.paginate(
        page = page,
        per_page = size,
        error_out = False
    )
    return jsonify({
        "data": [item.to_dict() for item in pagination.items],
        "page": page,
        "size": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    })


from sqlalchemy import text


@items_bp.route("/items/create")
@login_required
def create_item_page():
    user_id = session["user_id"]
    return render_template('demo_create_item.html', user_id=user_id)


@items_bp.route("/api/items", methods=["POST"])
def create_item():
    """

    JSON:
    {
        "itemName": "ITEM NAME",
        "description": "DESCRIPTION",
        "price": 11.4,
        "userId": 1,
        "image_url": "image url"
    }
    """
    data = request.get_json()


    if not data:
        return jsonify({"error": "No data provided"}), 400
    print(data)
    item_name = data.get("itemName")
    user_id = data.get("userId")

    if not item_name:
        return jsonify({"error": "Item name cannot be null"}), 400

    if not user_id:
        return jsonify({"error": "User ID cannot be null"}), 400

    user = User.query.get(user_id)
    print(user.to_dict())
    if not user:
        return jsonify({"error": "User does not exist"}), 404


    new_item = Item(
        itemName=item_name,
        userId=user_id,
        description=data.get("description", ""),
        price=data.get("price", 0.0),
        image_url=data.get("image_url", ""),
        is_available=data.get("is_available", True)
    )
    print(new_item.to_dict())



    try:
        db.session.add(new_item)
        db.session.flush()
        print(new_item.to_dict())
        user_item = UserItem(
            userid=user_id,
            itemid=new_item.itemId
        )
        db.session.add(user_item)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create item: {str(e)}"}), 500

    item_dict = new_item.to_dict()
    item_dict["owner_name"] = f"{user.firstName} {user.lastName}"

    return jsonify({
        "message": "Item created successfully",
        "item": item_dict
    }), 201

@items_bp.route("/api/items/<int:item_id>", methods=['GET'])
def get_item_detail(item_id):
    target = Item.query.get(item_id)
    data = target.to_dict()
    return jsonify(data)

@items_bp.route("/items/<item_id>")
def items_detail_page(item_id):
    return render_template('item_detail.html', item_id=item_id)


@items_bp.route("/api/items/<int:item_id>", methods=['PUT'])
def update_item(item_id):
    """
    更新物品信息

    JSON:
    {
        "itemName": "更新的物品名称",
        "description": "更新的描述",
        "price": 15.99,
        "image_url": "新的图片URL",
        "is_available": true
    }
    """
    try:
        # 获取要更新的物品
        item = Item.query.filter_by(itemId=item_id).first()
        if not item:
            return jsonify({"error": "Item not found"}), 404

        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # 更新物品字段（只更新提供的字段）
        if 'itemName' in data:
            item.itemName = data['itemName']
        if 'description' in data:
            item.description = data['description']
        if 'price' in data:
            item.price = data['price']
        if 'image_url' in data:
            item.image_url = data['image_url']
        if 'is_available' in data:
            item.is_available = data['is_available']

        # 提交更改
        Item.query.session.commit()

        # 获取物品拥有者信息
        user = User.query.filter_by(userId=item.userId).first()
        item_dict = item.to_dict()
        item_dict['owner_name'] = f"{user.firstName} {user.lastName}" if user else "Unknown"

        return jsonify({
            "message": "Item updated successfully",
            "item": item_dict
        }), 200

    except Exception as e:
        Item.query.session.rollback()
        return jsonify({"error": f"Failed to update item: {str(e)}"}), 500


@items_bp.route("/api/items/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
    """删除物品"""
    try:
        # 查找物品
        item = Item.query.filter_by(itemId=item_id).first()
        if not item:
            return jsonify({"error": "Item not found"}), 404

        # 检查是否有相关的订单
        existing_orders = Order.query.filter_by(itemId=item_id).first()
        if existing_orders:
            return jsonify({"error": "Cannot delete item with existing orders"}), 400

        # 删除 UserItem 关联
        user_items = UserItem.query.filter_by(itemid=item_id).all()
        for user_item in user_items:
            UserItem.query.session.delete(user_item)

        # 删除物品
        Item.query.session.delete(item)
        Item.query.session.commit()

        return jsonify({"message": "Item deleted successfully"}), 200

    except Exception as e:
        Item.query.session.rollback()
        return jsonify({"error": f"Failed to delete item: {str(e)}"}), 500


@items_bp.route("/api/items/user/<int:user_id>", methods=['GET'])
def get_user_items(user_id):
    """获取用户拥有的所有物品"""
    try:
        # 验证用户是否存在
        user = User.query.filter_by(userId=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)

        # 查询用户的物品
        query = Item.query.filter_by(userId=user_id)

        # 添加筛选条件（可选）
        is_available = request.args.get('is_available', type=str)
        if is_available:
            query = query.filter_by(is_available=(is_available.lower() == 'true'))

        # 分页
        pagination = query.paginate(
            page=page,
            per_page=size,
            error_out=False
        )

        # 构建返回数据
        items = []
        for item in pagination.items:
            item_dict = item.to_dict()
            item_dict['owner_name'] = f"{user.firstName} {user.lastName}"
            items.append(item_dict)

        return jsonify({
            "user_id": user_id,
            "user_name": f"{user.firstName} {user.lastName}",
            "page": page,
            "size": size,
            "total": pagination.total,
            "pages": pagination.pages,
            "items": items
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get user items: {str(e)}"}), 500


@items_bp.route("/api/items/available", methods=['GET'])
def get_available_items():
    """获取所有可用的物品"""
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 20, type=int)

        # 查询所有可用物品
        query = Item.query.filter_by(is_available=True)

        # 可选：按价格排序
        sort_by = request.args.get('sort_by', type=str)
        if sort_by == 'price_asc':
            query = query.order_by(Item.price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Item.price.desc())
        else:
            # 默认按创建时间排序（最新的在前）
            query = query.order_by(Item.itemId.desc())

        # 价格范围筛选
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        if min_price is not None:
            query = query.filter(Item.price >= min_price)
        if max_price is not None:
            query = query.filter(Item.price <= max_price)

        # 分页
        pagination = query.paginate(
            page=page,
            per_page=size,
            error_out=False
        )

        # 构建返回数据
        items = []
        for item in pagination.items:
            item_dict = item.to_dict()
            # 获取拥有者信息
            user = User.query.filter_by(userId=item.userId).first()
            item_dict['owner_name'] = f"{user.firstName} {user.lastName}" if user else "Unknown"
            item_dict['owner_email'] = user.email if user else None
            items.append(item_dict)

        return jsonify({
            "page": page,
            "size": size,
            "total": pagination.total,
            "pages": pagination.pages,
            "items": items
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get available items: {str(e)}"}), 500


@items_bp.route("/api/items/batch", methods=['POST'])
def create_batch_items():
    """
    批量创建物品

    JSON:
    {
        "userId": 1,
        "items": [
            {
                "itemName": "Item 1",
                "description": "Description 1",
                "price": 10.0,
                "image_url": "url1"
            },
            {
                "itemName": "Item 2",
                "description": "Description 2",
                "price": 20.0,
                "image_url": "url2"
            }
        ]
    }
    """
    try:
        data = request.get_json()

        if not data or not data.get('userId') or not data.get('items'):
            return jsonify({"error": "userId and items list are required"}), 400

        user_id = data.get('userId')
        items_data = data.get('items')

        # 验证用户
        user = User.query.filter_by(userId=user_id).first()
        if not user:
            return jsonify({"error": "User does not exist"}), 404

        created_items = []

        for item_data in items_data:
            if not item_data.get('itemName'):
                continue  # 跳过没有名称的物品

            # 创建新物品，让数据库自动分配ID
            new_item = Item()
            new_item.itemName = item_data.get('itemName')
            new_item.userId = user_id
            new_item.description = item_data.get('description', '')
            new_item.price = item_data.get('price', 0.0)
            new_item.image_url = item_data.get('image_url', '')
            new_item.is_available = item_data.get('is_available', True)

            Item.query.session.add(new_item)
            Item.query.session.flush()  # 刷新以获取自动生成的ID

            # 创建UserItem关联
            user_item = UserItem()
            user_item.userid = user_id
            user_item.itemid = new_item.itemId
            UserItem.query.session.add(user_item)

            created_items.append(new_item.to_dict())

        # 提交所有更改
        Item.query.session.commit()

        return jsonify({
            "message": f"Successfully created {len(created_items)} items",
            "items": created_items
        }), 201

    except Exception as e:
        Item.query.session.rollback()
        return jsonify({"error": f"Failed to create batch items: {str(e)}"}), 500


@items_bp.route("/api/items/fix-sequence", methods=['POST'])
def fix_item_sequence():
    """
    修复Item表的自增序列（仅适用于PostgreSQL）
    """
    try:
        # 获取当前最大的itemId
        max_item = Item.query.order_by(Item.itemId.desc()).first()

        if max_item:
            # 重置序列到最大ID + 1
            next_val = max_item.itemId + 1

            # PostgreSQL特定的序列重置命令
            Item.query.session.execute(
                text(f"""SELECT setval('lendscapev1."Item_itemid_seq"', :next_val, false)"""),
                {"next_val": next_val}
            )
            Item.query.session.commit()

            return jsonify({
                "message": f"Sequence fixed. Next ID will be {next_val}",
                "current_max_id": max_item.itemId,
                "next_id": next_val
            }), 200
        else:

            Item.query.session.execute(
                text("""SELECT setval('lendscapev1."Item_itemid_seq"', 1, false)""")
            )
            Item.query.session.commit()

            return jsonify({
                "message": "Sequence reset to 1",
                "next_id": 1
            }), 200

    except Exception as e:
        Item.query.session.rollback()
        return jsonify({
            "error": f"Failed to fix sequence: {str(e)}",
            "note": "This endpoint only works with PostgreSQL databases"
        }), 500
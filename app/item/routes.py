from flask import Blueprint, request, jsonify, render_template
from app import db
from app.item import items_bp
from app.models import User, Item
from decimal import Decimal


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

@items_bp.route("/api/items", methods=['POST'])
def create_item():
    pass


@items_bp.route("/page/items/search")
def search_page():
    return render_template('demo_search.html')



@items_bp.route("/api/items/<int:itemid>", methods=['GET'])
def get_item_detail(itemid):

    pass
from flask import Blueprint, request, jsonify, render_template
from app import db
from app.item import items_bp
from app.models import User, Item
from decimal import Decimal

@items_bp.route("/api/item_cnt", methods=["GET"])
def get_item_cnt():
    total_items = db.session.query(Item).count()

@items_bp.route("/api/items", methods=['GET'])
def get_items():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 20, type=int)

    kw = request.args.get("search", "", type=str).strip()

    query = Item.query
    if kw:
        results = Item.query.filter(
            Item.itemName.ilike(f"%{kw}%"),
            Item.is_available == True
        ).all()
    data = []
    for item in results:



@items_bp.route("/api/items", methods=['POST'])
def create_item():
    pass


@items_bp.route("/search")
def search_page():
    return render_template('demo_search.html')

@items_bp.route("/api/search_items", methods=["GET"])
def search_items():
    query = request.args.get("search", "").strip()

    if not query:
        return jsonify({
            "query": "",
            "count": 0,
            "results": []
        })

    results = Item.query.filter(
        Item.itemName.ilike(f"%{query}%"),
        Item.is_available == True
    ).all()
    print(Item.query.filter(
        Item.itemName.ilike(f"%{query}%"),
        Item.is_available == True
    ))
    print(results)
    data = []
    for item in results:
        item_dict = item.to_dict()
        user = User.query.get(item.userId)
        item_dict['owner_name'] = f"{user.firstName} {user.lastName}" if user else "Unknown"

        data.append(item_dict)

    return jsonify({
        "query": query,
        "count": len(data),
        "results": data
    })






from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.db import stores, items
import uuid

app_item = Blueprint("item", __name__, description="operation on Stores")


@app_item.route("/Item")
class Item(MethodView):
    def post(self):
        item_data = request.get_json()
        for item in items.values():
            if item["store_id"] not in stores:
                return {"message": "Item not found"}, 404

        item_id = uuid.uuid4().hex
        new_item = {"id": item_id, **item_data}
        items[item_id] = new_item
        return new_item

    def get(self):
        return {"items": list(items.values())}


@app_item.route("/Item/<string:item_id>")
class ItemById(MethodView):
    def put(self, item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            return abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.")
        try:
            items[item_id] = {**items[item_id], **item_data}
            return items[item_id]
        except KeyError:
            return abort(404, message="Item not found.")

    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            return {"message": "Item not found"}, 404

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found")

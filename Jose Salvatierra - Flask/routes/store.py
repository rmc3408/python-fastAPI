from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.db import stores
import uuid

app_store = Blueprint("stores", __name__, description="operation on Stores")


@app_store.route("/store/<string:score_id>")
class StoreById(MethodView):

    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            return abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")


@app_store.route("/store")
class Store(MethodView):

    def get(self):
        return {"stores": list(stores.values())}, 200

    def post(self):
        request_data = request.get_json()
        store_id = uuid.uuid4().hex
        new_store = {"id": store_id, **request_data}
        stores[store_id] = new_store
        return new_store, 201


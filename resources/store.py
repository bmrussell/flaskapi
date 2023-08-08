import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema, StoreUpdateSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[id]
        except KeyError:
            abort(404, message=f"Store {id} not found.")
    
    @blp.response(200, StoreSchema)
    def delete(self, id):
        try:
            del stores[id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message=f"Store {id} not found.")

    @blp.arguments(StoreUpdateSchema)
    def put(self, store_data, id):        
        try:        
            store = stores[id]
            store |= store_data   # |= is Dictionary update operator.
                                #  Changes contents of dictionary entry
            return {"message": "Store updated."}
        except KeyError:
            abort(404, message=f"Store {id} not found.")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):        
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists.")
                
        id = uuid.uuid4().hex
        new_store = {**store_data, "id": id}
        stores[id] = new_store

        return new_store
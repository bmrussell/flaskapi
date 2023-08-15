import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required # @jwt_required()
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError
from schemas import StoreSchema, StoreUpdateSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

###################################################################################
# /store/<string:id>
###################################################################################
@blp.route("/store/<string:id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, id):
        store = StoreModel.query.get_or_404(id)
        return store
    
    @jwt_required()
    @blp.response(200, StoreSchema)
    def delete(self, id):
        store = StoreModel.query.get_or_404(id)
        db.session.delete(store)
        db.session.commit()
        return {"message": f"Store {id} deleted"}

    @jwt_required()
    @blp.arguments(StoreUpdateSchema)
    def put(self, store_data, id):        
        store = StoreModel.query.get(id)
        if store:
            store.name = store_data["name"]
        else:
            store = StoreModel(id=id, **store_data)
            
        db.session.add(store)
        db.session.commit()
        return store

###################################################################################
# /store
###################################################################################
@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):        
        store = StoreModel(**store_data)
        
        try:
            db.session.add(store)
            db.session.commit()        
        except SQLAlchemyError as e:
            abort(500, f"A {type(e)} error occurred when inserting the store")
        
        return store
    
    
    
    
    
    
    
    
    
    
    
    
    
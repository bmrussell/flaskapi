from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from db import db
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")

###################################################################################
# /item/<string:id>
###################################################################################
@blp.route("/item/<string:id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, id):
        item = ItemModel.query.get_or_404(id)
        return item

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, id ):        
        item = ItemModel.query.get(id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=id, **item_data)
            
        db.session.add(item)
        db.session.commit()
        return item
    
    @jwt_required() 
    def delete(self, id):
        
        # Add authorization based on claim here
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401, message="Unathorized https://http.cat/401")
            
        item = ItemModel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Item {id} deleted"}


###################################################################################
# /item
###################################################################################
@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)               # Demand a fresh token for critical things
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):        
        item = ItemModel(**item_data)
        jwt = get_jwt()
        pass
        try:
            db.session.add(item)
            db.session.commit()        
        except SQLAlchemyError as e:
            abort(500, message=f"A {type(e)} error occurred when inserting the item")
        
        return item
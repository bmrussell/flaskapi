from flask.views import MethodView
from flask_smorest import Blueprint, abort

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
    @blp.response(200, ItemSchema)
    def get(self, id):
        item = ItemModel.query.get_or_404(id)
        return item

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
        
    def delete(self, id):
        item = ItemModel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Item {id} deleted"}


###################################################################################
# /item
###################################################################################
@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):        
        item = ItemModel(**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()        
        except SQLAlchemyError as e:
            abort(500, f"A {type(e)} error occurred when inserting the item")
        
        return item
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", __name__, description="Operations on tags")


@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)  # Query ORM for the store
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        # Check for the tag already present for this store
        # Not needed as we specified unique name in the model
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400, message=f"Tag {tag_data['name']} already exists for strore {store_id}")
            
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
            
        except SQLAlchemyError as e:
            abort(
                500, message=f"Failed to insert tag for strore {store_id} with {str(e)}"
            )

        return tag

@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        """_Link items and tags_

        Args:
            item_id (_string_): _description_
            tag_id (_string_): _description_
        """
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        # Validate item.store_id = tag.store_id
        if item.store.id != tag.store.id:
            abort(400, message="Make sure item and tag belong to the same store before linking.")
        
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"A {type(e)} error occured while inserting the tag {tag_id} ({e._message})")

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        """_Link items and tags_

        Args:
            item_id (_string_): _description_
            tag_id (_string_): _description_
        """
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        # Validate item.store_id = tag.store_id
        if item.store.id != tag.store.id:
            abort(400, message="Make sure item and tag belong to the same store before linking.")
        
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
            return {"message": "Item removed from tag", "item": item, "tag":tag}
        except SQLAlchemyError as e:
            abort(500, message=f"A {type(e)} error occured while removing the tag {tag_id} ({e._message})")

@blp.route("/tag/<string:id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, id):
        tag = TagModel.query.get_or_404(id)
        return tag
    
    @blp.response(202,description="Deletes a tag if no item is tagged with it.",example={"message": "Tag deleted."}, )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(400,description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",)    
    def delete(self, id):
        tag = TagModel.query.get_or_404(id)
        
        try:
            if not tag.items:
                db.session.delete(tag)
                db.session.commit()
                return {"message": "Tag deleted."}
        except SQLAlchemyError as e:
            abort(500, f"An error occurred when deleting the tag ({str(e)})")
            
        abort(400, message="Could not delete tag. Make sure tag is not linked to any items, then try again.")
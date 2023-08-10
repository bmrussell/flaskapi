from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import TagModel, StoreModel
from sqlalchemy.exc import SQLAlchemyError
from schemas import TagSchema

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

@blp.route("/tag/<string:id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, id):
        tag =TagModel.query.get_or_404(id)
        return tag

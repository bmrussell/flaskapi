from flask.views import MethodView
from flask_smorest import Blueprint, abort


blp = Blueprint("Healthchecks", __name__, description="Service Healthchecks")

###################################################################################
# /item/<int:id>
###################################################################################


@blp.route("/health")
class Health(MethodView):
    @blp.response(200)
    def get(self):
        return {"message": "OK"}

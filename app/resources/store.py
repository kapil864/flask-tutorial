
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import StoreSchema
from app.models.store import StoreModel
from app.db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# from app.db import stores


# used to divide an api into multiple segments
blp = Blueprint("stores", __name__, description="Operation on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store


    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return { "message" : "store deleted"}


@blp.route("/store")
class StoreList(MethodView):
    
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self,store_data):           

        store = StoreModel(**store_data)

        try : 
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(500, message="A store with taht name already")
        except SQLAlchemyError:
            abort(500, message="an error occured whuile inserting in db")
        return store

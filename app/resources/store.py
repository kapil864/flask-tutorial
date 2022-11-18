import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import StoreSchema
from db import stores


# used to divide an api into multiple segments
blp = Blueprint("stores", __name__, description="Operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort (404, message = "Store not found")



    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"description" : "Store deleted"}
        except KeyError:
            abort (400, message="Enter a valid store_id")



@blp.route("/store")
class StoreList(MethodView):
    
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self,store_data):           

        for store in stores.values():
            if store_data['name'] == store['name']:
                abort(400, message= f"Store already exists")

        store_id = uuid.uuid4().hex              
        store = {**store_data, "id":store_id}    
        stores[store_id] = store
        return store

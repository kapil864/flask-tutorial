
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import ItemSchema, ItemUpdateSchema
from db import items,stores


blp = Blueprint("Items", __name__, description="Opertation on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200,ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort (404, message = "Item not found")
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):

        try:
            item = items[item_id]
            item |= item_data    # update dictionary with item_data
            return items[item_id]
        except KeyError:
            abort(400, message="Item do not exist")

    
    def delete(self,item_id):
        try:
            del items[item_id]
            return {'description':'item deleted'}
        except KeyError:
            abort (400, message="Enter a valid item_id")




@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))   # converts dictionary to a list
    def get(self):
        return items.values()
    
    # to apply schemna
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self,item_data):             # item_data is obtained through schema (decorator) and it return a dictionart of validated data
        # item_data = request.get_json()  # no need as obtained through decorator

        # checks wether item already exists
        for item in items.values():
            if(
                item_data['name'] == item['name'] and
                item_data['store_id'] == item['store_id']
            ):
                abort (400, message="Item already exists")

        if item_data['store_id'] not in stores:
            abort (404, message = "Store not found")
        
        item_id = uuid.uuid4().hex               # generate a unique id
        item = {**item_data, "id":item_id}      # **store_data => create a dictionary from store_data
        items[item_id] = item
        return item, 201


import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items,stores


blp = Blueprint("items", __name__, description="Opertation on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort (404, message = "Item not found")
    
    def put(self, item_id):
        item_data = request.get_json()

        if(
            'price' not in item_data or
            'store_id' not in item_data or
            'name' not in item_data
        ):
            abort(
                400,
                message="Bad request ensure 'price', 'store_id' and 'name' are provided"
            )

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

    def get(self):
        return {"items" : list(items.values())}
    
    
    def post(self):
        item_data = request.get_json()

        if(
            'price' not in item_data or
            'store_id' not in item_data or
            'name' not in item_data
        ):
            abort(
                400,
                message=f"Bad request ensure 'price', 'store_id' and 'name' are provided"
            )

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

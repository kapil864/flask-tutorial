
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import ItemSchema, ItemUpdateSchema
from app.models.item import ItemModel
from app.models.store import StoreModel
from app.db import db
from sqlalchemy.exc import SQLAlchemyError
# from app.db import items,stores


blp = Blueprint("Items", __name__, description="Opertation on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):

    @blp.response(200,ItemSchema)
    def get(self, item_id):

        item = ItemModel.query.get_or_404(item_id)
        return item
            
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        
        item = ItemModel.query.get(item_id)


        if item:
            item.price = item_data['price']
            item.name = item['name']
        else:
            item = ItemModel(id= item_id,**item_data)
    
        db.session.add(item)
        db.session.commit()

        return item
    
    def delete(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message" : "item deleted"}


@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))   # converts dictionary to a list
    def get(self):
        return ItemModel.query.all()

    # to apply schemna
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self,item_data):             # item_data is obtained through schema (decorator) and it return a dictionart of validated data
        
        item = ItemModel(**item_data)

        try : 
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="an error occured whuile inserting in db")
        return item, 201
from app.db import db
from app.models.item_tags import items_tags

class TagModel(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(39), unique= False, nullable = False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable = False)

    store = db.relationship("StoreModel", back_populates ="tags")
    items = db.relationship("ItemModel", back_populates = "tags", secondary = items_tags)
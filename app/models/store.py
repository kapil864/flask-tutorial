
from app.db import db

class StoreModel(db.Model):

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)                    # deletes data that uses store id as foregin key    
    tags = db.relationship("TagModel", back_populates = "store", lazy = "dynamic")
    items = db.relationship("ItemModel", back_populates="store", lazy = "dynamic", cascade = "all, delete")
from app.db import db

# secodary Table
# class ItemsTag(db.Model):

#     __tablename__ = "items_tags"

#     id = db.Column(db.Integer, primary_key = True)
#     item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
#     tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))


# use the db.Table() function to create a table with two columns.
# For association tables,the best practice is to use a table instead of a database model

items_tags = db.Table("items_tags",
                        db.Column('id', db.Integer, primary_key = True),
                        db.Column("item_id", db.Integer, db.ForeignKey("items.id")),
                        db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"))
                        )
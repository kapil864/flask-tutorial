
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models.item import ItemModel
from app.schemas import TagSchema
from app.models.tag import TagModel
from app.models.store import StoreModel
from app.db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Tags", __name__, description = "Operations on Tags")

@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):

        # # to check incoming data weather it already exists in database
        # if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data['name']).first()
        #     abort (400, message = "A tag with that name already exists in taht store")

        tag = TagModel(**tag_data, store_id = store_id)

        try :
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message= str(e))

        return tag

@blp("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):

    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):

        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.qyery.get_or_404(tag_id)

        item.tags.append(tag)

        try :
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occured while inserting the tag")
        
        return tag


    @blp.response(201, TagSchema)
    def delete(self, item_id, tag_id):

        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.qyery.get_or_404(tag_id)

        item.tags.remove(tag)

        try :
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occured while inserting the tag")
        
        return {"message":"Item removed from tag", "item": item, "tag":tag}



@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag


    @blp.response(202, TagSchema, description="Delets a tag if no item is tagged with it", example={"message":"tag deleted"})
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(400, description="Returned if the tag is assigned to one or more items, In this case, tag is not deleted")  # alternative reponses
    def delete(self, tag_id):
        
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Tag deleted"}
        abort(
            400,
            message = "Could not delete tag, Make sure tag is not assosiated with any items, then try again"
        )


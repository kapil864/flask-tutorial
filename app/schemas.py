# for validation of payloads 

from marshmallow import Schema,fields


# Schema to be followed when inserting item (item post request)
class ItemSchema(Schema):
    id = fields.Str(dump_only=True)     # use only for returning data  # cannot be sent through api post request
    name = fields.Str(required=True)        # name should be a string
    price = fields.Float(required=True)     # price should be a float
    store_id = fields.Str(required=True)


# schema to be followed when updating existing item (put request)
class ItemUpdateSchema(Schema):
    name = fields.Str()       
    price = fields.Float()


# schema to be followed when inserting store (post request)
class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


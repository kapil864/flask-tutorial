# for validation of payloads 

from marshmallow import Schema,fields


# Schema to be followed when inserting item (item post request)
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)     # use only for returning data  # cannot be sent through api post request
    name = fields.Str(required=True)        # name should be a string
    price = fields.Float(required=True)     # price should be a float


# schema to be followed when updating existing item (put request)
class ItemUpdateSchema(Schema):
    name = fields.Str()       
    price = fields.Float()
    store_id = fields.Int()


# schema to be followed when inserting store (post request)
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only= True)           # only used when reciving  data from client
    store = fields.Nested(PlainStoreSchema(), dump_only = True)     # used whenr sending data to client
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only= True)

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only= True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only = True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only = True)  # do not send password to client
    
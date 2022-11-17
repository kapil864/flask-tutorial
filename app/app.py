

import uuid
from flask import Flask, request, abort
from db import items,stores
# from flask_smorest import abort

app = Flask(__name__)


# ENd points for store

@app.get('/store')
def get_stores():
    return {"stores" : list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()           # get data from post request
    if "name" not in store_data :
        abort(400, description="Ensure 'name' is included in JSON payload")
    
    for store in stores.values():
        if store_data['name'] == store['name']:
            abort(400,  description= f"Store already exists")

    store_id = uuid.uuid1()               # generate a unique id
    store = {**store_data, "id":store_id}    # **store_data => create a dictionary from store_data
    stores[store_id] = store
    return store


@app.get('/store/<string:store_id>')   # a parameter is sent
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort (404, description = "Store not found")

@app.put('/store/<string:store_id>')
def edit_store(store_id):
    store_data = request.get_json()
    if ('store_id' not in store_data or 'name' not in store_data):
        abort(400, description="Ensure 'store_id'and 'name' is included in JSON pay load")
    
    try:
        stores[store_id]['name'] = store_data['name']
    except KeyError:
        abort (400, description="Enter a valid store_id")
    
    return stores['store_id']

@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"description" : "Store deleted"}
    except KeyError:
        abort (400, description="Enter a valid store_id")


# Items endpoints

@app.post('/item')  
def create_item():
    item_data = request.get_json()

    if(
        'price' not in item_data or
        'store_id' not in item_data or
        'name' not in item_data
    ):
        abort(
            400,
            description=f"Bad request ensure 'price', 'store_id' and 'name' are provided"
        )

    for item in items.values():
        if(
            item_data['name'] == item['name'] and
            item_data['store-id'] == item['store_id']
        ):
            abort (400, description="Item already exists")

    if item_data['store_id'] not in stores:
        abort (404, description = "Store not found")
    
    item_id = uuid.uuid().hex               # generate a unique id
    item = {**item_data, "id":item_id}    # **store_data => create a dictionary from store_data
    items[item_id] = item
    return item, 201


@app.get('/item')
def get_items():
    return {"items" : list(items.values())}


@app.get('/item/<string:item_id>')   # a parameter is sent
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort (404, description = "Item not found")


@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {'description':'item deleted'}
    except KeyError:
        abort (400, description="Enter a valid item_id")


@app.put('/item/<string:item_id>')   # a parameter is sent
def edit_item(item_id):
    item_data = request.get_json()

    if(
        'price' not in item_data or
        'store_id' not in item_data or
        'name' not in item_data
    ):
        abort(
            400,
            description="Bad request ensure 'price', 'store_id' and 'name' are provided"
        )

    try:
        item = items[item_id]
        item |= item_data    # update dictionary with item_data
        return items[item_id]
    except KeyError:
        abort(400, description="Item do not exist")
    
    

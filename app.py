
from flask import Flask, request

app = Flask(__name__)

stores = [
    {
       'name':'my store',
        'items' : [
            {
                'name':'chair',
                'price':15.99
            }
        ]
    }
]

@app.get('/store')
def get_stores():
    return {"stores" : stores}

@app.post("/store")
def create_store():
    request_data = request.get_json()           # get data from post request
    new_store = {"name" : request_data['name'], 'items' :request_data['items']}
    stores.append(new_store)
    return new_store, 201

@app.post('/store/<string:name>/item')   # a parameter is sent
def create_item(name):
    request_data = request.get_json()
    new_item = {"name" : request_data['name'], "price" : request_data['price'] }
    for store in stores :
        if name == store['name']:
            store['items'].append(new_item)
            return store
    return {"message":"Store not found"}, 404


@app.get('/store/<string:name>/item')   # a parameter is sent
def get_item(name):
    for store in stores :
        if name == store['name']:
            return {'items':store['items']}
    return {"message":"Store not found"}, 404
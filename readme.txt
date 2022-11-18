docker run -d -p 5000:5000 -w /app -v "$PWD:/app" --name udemy-tutorial-container udemy-tutorial

Syncs current folder to the folder in container. i.e creates a volume
Enables automatic reloading inside the container

Marshmellow for data validation

# to apply schemna
@blp.arguments([ schema name])
@blp.response([scheman name])         => apply a schema when api return data (get request is made) , reponse should be put after arguments
def post/get/put ;;;; method to apply schema to 
    store_data = request.get_json() # it is removed as data is validated through schema (decorator) and it returnna a dictionary


@blp.response(200, ItemSchema(many=True))   # converts dictionary to a list
    def get(self):
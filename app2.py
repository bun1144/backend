from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from flask_cors import CORS ,cross_origin
uri = "mongodb+srv://kitti:bun12345@cluster0.bxs0qg3.mongodb.net/"
client = MongoClient(uri)
db = client["product"]
collection = db["product_info"]
p_in_DB = collection.find()
products=[]
for p in p_in_DB:
    products.append(p)

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/products",methods=["GET"])
def get_all_products():
    return jsonify(products),200

@app.route("/products",methods=["POST"])
@cross_origin()
def add_product():
    data = request.get_json(products)
    count = 0
    temp = 0
    if products:
        print("it empty!!!!")
    for _ in products :
        count = _   
        temp = temp+1
   
    ttt = 0
    if temp != 0 :
        ttt = count["_id"]+1
    new_product = {
        "_id":ttt,
        "name":data["name"],
        "price":data["price"],
    }
    products.append(new_product)
    collection.insert_one({
        "_id":ttt,
        "name":data["name"],
        "price":data["price"]
    })
    return jsonify(products),200
    
@app.route("/products/<int:id>",methods=["DELETE"])
def detele_product(id):
    for d in products:
        if(d["_id"] == id):
            products.remove(d)
            collection.delete_one({"_id":id})
            return jsonify(products),200
    return jsonify(products),404
    
@app.route("/products/<int:id>",methods=["PUT"])
def update_product(id):
    data = request.get_json(products)
    up_p = {
        "_id":{id},
        "name":data["name"],
        "price":data["price"],
    }
    for a in products:
        if(a["_id"] == id):
            a.update(data)
            collection.update_many(
                {"_id":a["_id"]},
                {"$set":{   "name" : data["name"],
                            "price" : data["price"]
                        }
                }
            )
            return jsonify(products),200
    return jsonify("Not found!!"),200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
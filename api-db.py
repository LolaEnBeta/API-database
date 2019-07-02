from flask import Flask, jsonify, request, make_response, abort
import sqlite3
from user import User
from dogs import Dogs
import UserRepository

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world!!"

@app.route("/users", methods=["POST"])
def create_user():

    if not "name" in request.json or not "age" in request.json:
        abort(400)

    name = request.json.get("name")
    age = request.json.get("age")

    try:
        age = int(age)
    except:
        print("This is not a number")
        exit()

    user = User(None, name, age)
    result = UserRepository.add(user)
    return result

@app.route("/dogs", methods=["POST"])
def create_dog():
    if not "name" in request.json or not "human_id" in request.json:
        abort(400)
    name = request.json.get("name")
    human_id = request.json.get("human_id")

    try:
        human_id = int(human_id)
    except:
        print("This is not a number")
        exit()

    human = UserRepository.get_by_id(human_id)
    if not human:
        abort(404)

    dog = Dogs(None, name, human_id)
    result = UserRepository.add_dog(dog)
    return result

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = UserRepository.get_by_id(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_json())

@app.route("/dogs/<int:dog_id>", methods=["GET"])
def get_dog_by_id(dog_id):
    dog = UserRepository.get_dog_by_id(dog_id)
    if not dog:
        abort(404)
    return jsonify(dog.to_json())

@app.route("/users", methods=["GET"])
def get_users():
    users = UserRepository.get_all()
    users_list = []
    for user in users:
        users_list.append(user.to_json())
    return jsonify(users_list)

@app.route("/dogs", methods=["GET"])
def get_all_dogs():
    dogs = UserRepository.get_all_dogs()
    dogs_list = []
    for dog in dogs:
        dogs_list.append(dog.to_json())
    return jsonify(dogs_list)

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    result = UserRepository.delete_by_id(user_id)
    if not result:
        abort(404)
    return result

@app.route("/users/<int:user_id>", methods=["PUT"])
def modify_user_by_id(user_id):
    if not "age" in request.json:
        abort(400)

    age = request.json.get("age")

    user = UserRepository.modify_by_id(user_id, age)

    return jsonify(user.to_json())

@app.errorhandler(400)
def bad_request(error):
    return make_response("bad request", 400)

@app.errorhandler(404)
def not_found(error):
    return make_response("not found", 404)

if __name__ == "__main__":
    app.run(debug=True)

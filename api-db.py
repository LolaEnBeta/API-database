from flask import Flask, jsonify, request, make_response, abort
import sqlite3
from user import User
from dog import Dog
import UserRepository
import DogRepository

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

    human = DogRepository.get_by_id(human_id)
    if not human:
        abort(404)

    dog = Dog(None, name, human_id)
    result = DogRepository.add_dog(dog)
    return result

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = UserRepository.get_by_id(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_json())

@app.route("/dogs/<int:dog_id>", methods=["GET"])
def get_dog_by_id(dog_id):
    dog = DogRepository.get_dog_by_id(dog_id)
    if not dog:
        abort(404)
    return jsonify(dog.to_json())

@app.route("/users", methods=["GET"])
def get_users():
    users = UserRepository.get_all()
    users_list = [user.to_json() for user in users]
    return jsonify(users_list)

@app.route("/dogs", methods=["GET"])
def get_all_dogs():
    dogs = DogRepository.get_all_dogs()
    dogs_list = [dog.to_json() for dog in dogs]
    return jsonify(dogs_list)

@app.route("/users/<int:user_id>", methods=["DELETE"])
def remove_user_by_id(user_id):
    result = UserRepository.delete_by_id(user_id)
    if not result:
        abort(404)
    return result

@app.route("/dogs/<int:dog_id>", methods=["DELETE"])
def remove_dog_by_id(dog_id):
    result = DogRepository.remove_dog_by_id(dog_id)
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

@app.route("/dogs/<int:dog_id>", methods=["PUT"])
def modify_dog_by_id(dog_id):
    if not "name" in request.json and not "human_id" in request.json:
        abort(400)

    dog = DogRepository.get_dog_by_id(dog_id)
    if not dog:
        abort(404)

    name = request.json.get("name", dog.name)
    human_id = request.json.get("human_id", dog.human_id)

    dog_modified = DogRepository.modify_dog_by_id(dog_id, name, human_id)
    return jsonify(dog_modified.to_json())

@app.route("/users/<int:user_id>/dogs", methods=["GET"])
def get_human_dog_relation(user_id):

    user = UserRepository.get_by_id(user_id)

    if not user:
        abort(404)

    relation = UserRepository.get_human_dog_relation(user)
    return jsonify(relation)

@app.errorhandler(400)
def bad_request(error):
    return make_response("bad request", 400)

@app.errorhandler(404)
def not_found(error):
    return make_response("not found", 404)

if __name__ == "__main__":
    app.run(debug=True)

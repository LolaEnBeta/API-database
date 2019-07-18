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
        return make_response(jsonify("This is not a number"), 400)

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

    human = UserRepository.get_by(human_id)
    if not human:
        abort(404)

    dog = Dog(None, name, human_id)
    result = DogRepository.add(dog)
    return result

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = UserRepository.get_by(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_json())

@app.route("/dogs/<int:dog_id>", methods=["GET"])
def get_dog_by_id(dog_id):
    dog = DogRepository.get_by(dog_id)
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
    dogs = DogRepository.get_all()
    dogs_list = [dog.to_json() for dog in dogs]
    return jsonify(dogs_list)

@app.route("/users/<int:user_id>", methods=["DELETE"])
def remove_user_by_id(user_id):

    user = UserRepository.get_by(user_id)
    if not user:
        abort(404)

    try:
        UserRepository.remove(user)
        return "user deleted"
    except:
        abort(500)

@app.route("/dogs/<int:dog_id>", methods=["DELETE"])
def remove_dog_by_id(dog_id):

    dog = DogRepository.get_by(dog_id)

    if not dog:
        abort(404)

    try:
        DogRepository.remove(dog)
        return "dog deleted"
    except:
        abort(500)

@app.route("/users/<int:user_id>", methods=["PUT"])
def modify_user_by_id(user_id):
    if not "age" in request.json:
        abort(400)

    user = UserRepository.get_by(user_id)
    if not user:
        abort(404)

    age = request.json.get("age")
    user.age = age

    try:
        UserRepository.modify(user)
        return jsonify(user.to_json())
    except:
        abort(500)

@app.route("/dogs/<int:dog_id>", methods=["PUT"])
def modify_dog_by_id(dog_id):

    if not "name" in request.json and not "human_id" in request.json:
        abort(400)

    dog = DogRepository.get_by(dog_id)
    if not dog:
        abort(404)

    name = request.json.get("name", dog.name)
    human_id = request.json.get("human_id", dog.human_id)

    dog.name = name
    dog.human_id = human_id

    try:
        DogRepository.modify(dog)
        return jsonify(dog.to_json())
    except:
        abort(500)

@app.route("/users/<int:user_id>/dogs", methods=["GET"])
def get_user_dog_relation_by_user_id(user_id):

    user = UserRepository.get_by(user_id)

    if not user:
        abort(404)

    relation = UserRepository.get_user_dog_relation(user)
    return jsonify(relation)

@app.route("/dogs/<int:dog_id>/users", methods=["GET"])
def get_dog_user_relation_by_dog_id(dog_id):
    dog = DogRepository.get_by(dog_id)
    if not dog:
        abort(404)

    relation = DogRepository.get_dog_user_relation(dog)
    return jsonify(relation)

@app.errorhandler(400)
def bad_request(error):
    return make_response("bad request", 400)

@app.errorhandler(404)
def not_found(error):
    return make_response("not found", 404)

@app.errorhandler(500)
def internal_server_error(error):
    return make_response("internal server error", 500)

if __name__ == "__main__":
    app.run(debug=True)

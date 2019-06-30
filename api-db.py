from flask import Flask, jsonify, request, make_response, abort
import sqlite3
from user import User
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

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = UserRepository.get_by_id(user_id)
    if not user:
        abort(404)
    return jsonify({"user": user.to_json()})

@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect("sqlite3/database.db")

    query = conn.cursor()

    sql = "SELECT * FROM users"

    if (query.execute(sql)):
        rows = query.fetchall()
        users = []
        for row in rows:
            get_user = User(row[0], row[1], row[2])
            users.append(get_user.to_json())
        return jsonify({"users": users})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    conn = sqlite3.connect("sqlite3/database.db")

    query = conn.cursor()

    sql = "SELECT * FROM users WHERE id = %s" % user_id

    if (query.execute(sql)):
        user = query.fetchone()
        if not user:
            abort(404)

    sql = "DELETE FROM users WHERE id = %s" % user_id

    if (query.execute(sql)):
        query.close()
        conn.commit()
        conn.close()
        return "user deleted"

@app.route("/users/<int:user_id>", methods=["PUT"])
def modify_user_by_id(user_id):
    conn = sqlite3.connect("sqlite3/database.db")

    query = conn.cursor()

    sql = "SELECT * FROM users WHERE id = %s" % user_id

    if (query.execute(sql)):
        user = query.fetchone()
        get_user = User(user[0], user[1], user[2])
        if not user:
            abort(404)

    if not "age" in request.json:
        abort(400)

    get_user.age = request.json.get("age")

    sql = "UPDATE users SET age = ? WHERE id = ?"

    arguments = (get_user.age, user_id)

    if (query.execute(sql, arguments)):
        query.close()
        conn.commit()
        conn.close()
        return jsonify({"user modified": get_user.to_json()})

@app.errorhandler(400)
def bad_request(error):
    return make_response("bad request", 400)

@app.errorhandler(404)
def not_found(error):
    return make_response("not found", 404)

if __name__ == "__main__":
    app.run(debug=True)

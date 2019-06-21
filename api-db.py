from flask import Flask, jsonify, request, make_response, abort
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world!!"

@app.route("/users", methods=["POST"])
def create_user():
    conn = sqlite3.connect("***/***.db")

    query = conn.cursor()

    if not "name" in request.json or not "age" in request.json:
        abort(400)

    name = request.json.get("name")
    age = request.json.get("age")

    try:
        age = int(age)
    except:
        print("This is not a number")
        exit()

    arguments = (name, age)

    sql = """
    INSERT INTO users (name, age)
    VALUES (?, ?)
    """

    if (query.execute(sql, arguments)):
        query.close()
        conn.commit()
        conn.close()
        return "User created successfully"
    else:
        return "An error has ocurred"

@app.errorhandler(400)
def bad_request(error):
    return make_response("bad request", 400)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_users(user_id):
    conn = sqlite3.connect("***/***.db")

    query = conn.cursor()

    sql = "SELECT * FROM users WHERE id = %s" % user_id

    if (query.execute(sql)):
        user = query.fetchone()
        if not user:
            abort(404)
        query.close()
        conn.commit()
        conn.close()
        return jsonify({"user": user})

    else:
        return "An erros has ocurred"

@app.errorhandler(404)
def not_found(error):
    return make_response("not found", 404)

if __name__ == "__main__":
    app.run(debug=True)

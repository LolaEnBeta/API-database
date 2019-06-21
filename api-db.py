from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world!!"

@app.route("/users", methods=["POST"])
def create_user():
    conn = sqlite3.connect("***/***.db")

    query = conn.cursor()

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

@app.route("/users/<int:user_id>", methods=["GET"])
def get_users(user_id):
    conn = sqlite3.connect("***/***.db")

    query = conn.cursor()

    sql = "SELECT * FROM users WHERE id = %s" % user_id

    if (query.execute(sql)):
        user = query.fetchone()
        query.close()
        conn.commit()
        conn.close()
        return jsonify({"user": user})

    else:
        return "An erros has ocurred"

if __name__ == "__main__":
    app.run(debug=True)

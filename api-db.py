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
        return "User created successfully"
    else:
        return "An error has ocurred"

if __name__ == "__main__":
    app.run(debug=True)

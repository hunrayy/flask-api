from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
# print(MySQL)

# print(Flask)
server = Flask(__name__)
server.config["MYSQL_HOST"] = "localhost"
server.config["MYSQL_USER"] = "root"
server.config["MYSQL_PASSWORD"] = ""
server.config["MYSQL_DB"] = "dynamo_db"
mysql = MySQL(server)
# home page route
@server.route("/", methods=["GET"])
def homepage():
    if(request.method == "GET"):
        cur = mysql.connection.cursor()
        sql = cur.execute("SELECT * FROM `users`")
        if(sql):
            mysql.connection.commit()
            return jsonify(cur.fetchall())
        # return jsonify({
        #     "message": "welcome",
        #     "code": "success"
        # })
    return "COULD NOT LOAD PAGE"


@server.route("/home", methods=["GET"])
def home():
    return render_template("home.html")



@server.route("/databaseset", methods=["POST"])
def createDB():
    cur = mysql.connection.cursor()
    if(cur):
        cur.execute(f"""CREATE TABLE `users` (
                    `id` NOT NULL AUTO_INCREMENT INT,
                    `firstname` NOT NULL VARCHAR(200),
                    `lastname` NOT NULL VARCHAR(200),
                    `email` NOT NULL UNIQUE VARCHAR(200),
                    `password` NOT NULL VARCHAR(200),
                    `cf_password` NOT NULL VARCHAR(200)
                    )""")
        return "connected successfully"
    return "could not connect"





@server.route("/register", methods=['POST'])
def regUser():
    fname = request.json(['fname'])
    password = request.json
    return jsonify({
        "fname":fname,
        "password":password
    })

if(__name__ == '__main__'):
    server.run(debug=True)
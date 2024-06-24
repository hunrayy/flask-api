from flask import Flask, jsonify, request, render_template, session
from flask_mysqldb import MySQL
import bcrypt


server = Flask(__name__)
server.secret_key = "your_secret_key"
server.config["MYSQL_HOST"] = "localhost"
server.config["MYSQL_USER"] = "root"
server.config["MYSQL_PASSWORD"] = ""
server.config["MYSQL_DB"] = "dynamo_db"
mysql = MySQL(server)

# home page route
@server.route("/", methods=["GET"])
def homepage():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        sql = cur.execute("SELECT * FROM users")
        if sql:
            mysql.connection.commit()
            return jsonify(cur.fetchall())
    return "COULD NOT LOAD PAGE"


@server.route("/home", methods=["GET"])
def home():
    return render_template("home.html")


@server.route("/databaseset", methods=["POST"])
def createDB():
    cur = mysql.connection.cursor()
    if cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            firstname VARCHAR(100) NOT NULL,
            lastname VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        mysql.connection.commit()
        cur.close()
        return "connected successfully"
    return "could not connect"


@server.route("/register", methods=['POST'])
def regUser():
    data = request.json
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')
    cf_password = data.get('cf_password')
    
    if not firstname or not lastname or not email or not password or not cf_password:
        return jsonify({"error": "All fields are required"}), 400

    if password != cf_password:
        return jsonify({"error": "Passwords do not match"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)",
                    (firstname, lastname, email, hashed_password))
        mysql.connection.commit()
        
        # Create a session
        session['email'] = email
        session['firstname'] = firstname
        session['lastname'] = lastname
        
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
    
    return jsonify({
        "message": "account successfully created",
        "code": "success",
        "data": {
            "firstname": firstname,
            "lastname": lastname,
            "email": email
        }
    }), 201



@server.route("/login", methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    if user and bcrypt.checkpw(password.encode("utf-8"), user[4].encode("utf-8")):  
        session['email'] = user[3]
        session['firstname'] = user[1]
        session['lastname'] = user[2]
        return jsonify({"message": "Login successful", "code": "success"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

if __name__ == '__main__':
    server.run(debug=True)





























# from flask import Flask, jsonify, request, render_template
# from flask_mysqldb import MySQL

# from flask_session import Session

# # print(MySQL)

# # print(Flask)
# server = Flask(__name__)
# server.config["MYSQL_HOST"] = "localhost"
# server.config["MYSQL_USER"] = "root"
# server.config["MYSQL_PASSWORD"] = ""
# server.config["MYSQL_DB"] = "dynamo_db"
# server.config["SECRET_KEY"] = "ghj6g@hdg86svs*gva#cbc%v67c2gc2"  
# server.config["SESSION_TYPE"] = "filesystem"
# mysql = MySQL(server)
# Session(server)

# # home page route
# @server.route("/", methods=["GET"])
# def homepage():
#     if(request.method == "GET"):
#         cur = mysql.connection.cursor()
#         sql = cur.execute("SELECT * FROM `users`")
#         if(sql):
#             mysql.connection.commit()
#             return jsonify(cur.fetchall())
#         # return jsonify({
#         #     "message": "welcome",
#         #     "code": "success"
#         # })
#     return "COULD NOT LOAD PAGE"


# @server.route("/home", methods=["GET"])
# def home():
#     return render_template("home.html")



# @server.route("/databaseset", methods=["POST"])
# def createDB():
#     cur = mysql.connection.cursor()
#     if(cur):
#         cur.execute(f"""CREATE TABLE `users` (
#                     `id` NOT NULL AUTO_INCREMENT INT,
#                     `firstname` NOT NULL VARCHAR(200),
#                     `lastname` NOT NULL VARCHAR(200),
#                     `email` NOT NULL UNIQUE VARCHAR(200),
#                     `password` NOT NULL VARCHAR(200),
#                     `cf_password` NOT NULL VARCHAR(200)
#                     )""")
#         return "connected successfully"
#     return "could not connect"





# @server.route("/register", methods=['POST'])
# def regUser():
#     data = request.json
#     firstname = data.get('firstname')
#     lastname = data.get('lastname')
#     email = data.get('email')
#     password = data.get('password')
#     cf_password = data.get('cf_password')
    
#     if not firstname or not lastname or not email or not password or not cf_password:
#         return jsonify({"error": "All fields are required"}), 400

#     if password != cf_password:
#         return jsonify({"error": "Passwords do not match"}), 400

#     cur = mysql.connection.cursor()
#     try:
#         cur.execute("INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)",
#                     (firstname, lastname, email, password))
#         mysql.connection.commit()
#         cur.close()

#         # Create a session
#         session['email'] = email
#         session['firstname'] = firstname
#         session['lastname'] = lastname
#     except Exception as e:
#         mysql.connection.rollback()
#         return jsonify({"error": str(e)}), 500
#     finally:
#         cur.close()
    
#     return jsonify({
#         "message": "account successfully created",
#         "code": "success",
#         "data": {
#             "firstname": firstname,
#             "lastname": lastname,
#             "email": email,
#             "password": password
#         }
#     }), 201


# @server.route("/login", methods=['POST'])
# def login():
#     data = request.json
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"error": "Email and password are required"}), 400

#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM users WHERE email = %s", (email,))
#     user = cur.fetchone()
#     cur.close()

#     if user and check_password_hash(user[4], password):  # assuming the password is stored in the 5th column
#         session['email'] = user[3]
#         session['firstname'] = user[1]
#         session['lastname'] = user[2]
#         return jsonify({"message": "Login successful", "code": "success"}), 200
#     else:
#         return jsonify({"error": "Invalid email or password"}), 401


# if(__name__ == '__main__'):
#     server.run(debug=True)
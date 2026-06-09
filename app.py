from flask import Flask, render_template, request, g, jsonify, session, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.config["SECRET_KEY"] = "magistratura"

def get_all_users():
    cursor = g.conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()
    return data

def get_all_messages(user1, user2):
    cursor = g.conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE ownerId=%s AND deliverId=%s OR deliverId=%s AND ownerId=%s",user1,user2,user1,user2)
    data = cursor.fetchall()
    cursor.close()
    return data


"""@app.before_request
def connect():
    conn = mysql.connector.connect(
        host="185.114.247.43",
        database="sch688_magistratura",
        user="sch688_magistratura",
        password="Qwerty123")
    g.conn = conn

@app.teardown_request
def close_connect(er):
    g.conn.close()"""

@app.route("/")
def index():
    return render_template("registration.html")

@app.route("/enter")
def registration():
    return render_template("avtorization.html")

@app.route("/chat")
def profile():
    if "user_id" in session:
        cursor = g.conn.cursor()
        id_ = session["user_id"]
        cursor.execute("SELECT * FROM users WHERE id=%s",(id_,))
        data = cursor.fetchone()
        all_users = get_all_users()
        user2_id = request.args.get("id")
        cursor.execute("SELECT * FROM users WHERE id=%s",(user2_id,))
        user2=cursor.fetchone()
        messages = get_all_messages(id_,user2_id)
        cursor.close()
        return render_template("chat.html", owner = data, deliver=user2, all_users=all_users, messages = messages)
    else:
        return render_template("avtrization.html")

@app.route("/user_registration", methods=["POST"])
def user_registration():
    data = request.json
    cursor = g.conn.cursor()
    cursor.execute("SELECT id FROM users WHERE login = %s", (data["login"],))
    cursor.execute("INSERT INTO users (name, surname, login, password) VALUES (%s,%s,%s,%s)",
                   (data["name"], data["surname"], data["login"], hashed_pw))
    g.conn.commit()
    new_user_id = cursor.lastrowid
    cursor.close()
    return jsonify({"user_id": new_user_id, "code": 200})

@app.route("/user_avtorization", methods=["POST"])
def user_avtorization():
    data = request.json
    login = data["login"]
    pas = data["password"]
    cursor = g.conn.cursor()
    cursor.execute("SELECT * from users WHERE login=%s", (login,))
    user = cursor.fetchall()
    cursor.close()
    if user:
        if pas == user [0][4]:
            session["user_login"] = user[0][3]
            session["user_id"] = user[0][0]
            return jsonify({"result": True,"message": "avtorization ok", "code": 200})
        else:
            return jsonify({"result": False,"message": "wrong password", "code": 400})
    else:
        return jsonify({"result": False,"message": "user not in bd", "code": 400})
    
@app.route("/send_mes", methods=["POST"])
def send_mes():
    data = request.json
    cursor = g.conn.cursor()
    cursor.execute("INSERT INTO messages (ownerId, deliverId, text, date) VALUES (%s,%s,%s)",
                   (data["owner"],data["deliver"],data["text"]))
    g.conn.commit()
    new_mes_id = cursor.lastrowid
    cursor.close
    return jsonify({"result": True,"mes_id": new_mes_id, "code": 200})

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_login", None)
    return redirect(url_for("/enter"))
app.run()
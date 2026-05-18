from flask import Flask, render_template, request, g, jsonify
import mysql.connector, hashlib

def hash_to_32chars(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

app = Flask(__name__)

'''@app.before_request
def connect():
    conn = mysql.connector.connect(
        host="185.114.247.43",
        database="sch688_magistratura",
        user="sch688_magistratura",
        password="Qwerty123")
    g.conn = conn

@app.teardown_request
def close_connect(er):
    g.conn.close()'''

@app.route("/")
def index():
    return render_template("registration.html")

@app.route("/login")
def registration():
    return render_template("avtorization.html")

@app.route("/chat")
def show_chat():
    cursor = g.conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT messages.content, messages.created_at, users.login 
        FROM messages 
        JOIN users ON messages.user_id = users.id 
        ORDER BY messages.created_at ASC
    """)
    messages = cursor.fetchall()
    cursor.close()
    return render_template("chat.html", messages=messages)

@app.route("/send_message", methods=["POST"])
def send_message():
    if not hasattr(g, 'user_id'):
        return "Не авторизован", 403
    content = request.form.get("content")
    if content:
        cursor = g.conn.cursor()
        cursor.execute("INSERT INTO messages (user_id, content) VALUES (%s, %s)", (g.user_id, content))
        g.conn.commit()
        cursor.close()
    return redirect(url_for("show_chat"))

@app.route("/user_registration", methods=["POST"])
def user_registration():
    data = request.json
    cursor = g.conn.cursor()
    cursor.execute("SELECT id FROM users WHERE login = %s", (data["login"],))
    if cursor.fetchone():
        return jsonify({"error": "Логин уже занят", "code": 400}), 400
    hashed_pw = hash_to_32chars(data["password"])
    cursor.execute("INSERT INTO users (name, surname, login, password) VALUES (%s,%s,%s,%s)",
                   (data["name"], data["surname"], data["login"], hashed_pw))
    g.conn.commit()
    new_user_id = cursor.lastrowid
    cursor.close()
    return jsonify({"user_id": new_user_id, "code": 200})

app.run()
from flask import Flask, render_template, request, g, jsonify, session, redirect, url_for
import pymysql
from pymysql import Error   # Импортируем класс ошибок PyMySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "magistratura"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def get_all_users():
    cursor = g.conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()
    return data

def get_all_messages(user1, user2):
    cursor = g.conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE ownerId=%s AND deliverId=%s OR deliverId=%s AND ownerId=%s",(user1,user2,user1,user2))
    data = cursor.fetchall()
    cursor.close()
    return data


@app.before_request
def connect():
    try:
        g.conn = pymysql.connect(
            host="185.114.247.43",
            database="sch688_magistratura",
            user="sch688_magistratura",
            password="Qwerty123",
            cursorclass=pymysql.cursors.DictCursor
        )
    except Error as e:
        print(f"❌ PyMySQL connection error: {e}")
        g.conn = None

@app.teardown_request
def close_connect(error=None):
    conn = getattr(g, 'conn', None)
    if conn is not None:
        try:
            conn.close()
        except Exception as e:
            print(f"Error closing connection: {e}")

@app.route("/")
def index():
    return render_template("registration.html")

@app.route("/enter")
def registration():
    return render_template("avtorization.html")

@app.route("/chat")
@login_required
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
        return render_template("avtorization.html")

@app.route("/user_registration", methods=["POST"])
def user_registration():
    data = request.json
    cursor = g.conn.cursor()
    
    # Проверка уникальности логина
    cursor.execute("SELECT id FROM users WHERE login = %s", (data["login"],))
    if cursor.fetchone():
        cursor.close()
        return jsonify({"result": False, "message": "Логин уже существует", "code": 400})
    
    # Хеширование пароля
    hashed_password = generate_password_hash(data["password"])
    
    cursor.execute("INSERT INTO users (name, surname, login, password) VALUES (%s,%s,%s,%s)",
                   (data["name"], data["surname"], data["login"], hashed_password))
    g.conn.commit()
    new_user_id = cursor.lastrowid
    cursor.close()
    
    # Автоматическая авторизация
    session["user_id"] = new_user_id
    session["user_login"] = data["login"]
    
    return jsonify({"result": True, "code": 200})

@app.route("/user_avtorization", methods=["POST"])
def user_avtorization():
    data = request.json
    login = data["login"]
    pas = data["password"]
    print(f"Login attempt: {login}, password: {pas}")  # отладка
    
    cursor = g.conn.cursor()
    cursor.execute("SELECT * FROM users WHERE login=%s", (login,))
    user = cursor.fetchone()  # важно: fetchone, а не fetchall
    cursor.close()
    
    if not user:
        print("User not found")
        return jsonify({"result": False, "message": "user not in bd", "code": 400})
    
    print(f"Stored password from DB: {user['password']}")
    print(f"Type of stored password: {type(user['password'])}")
    
    # Проверка
    if check_password_hash(user["password"], pas):
        print("Password matches")
        session["user_login"] = user["login"]
        session["user_id"] = user["id"]
        return jsonify({"result": True, "message": "avtorization ok", "code": 200})
    else:
        print("Password does NOT match")
        return jsonify({"result": False, "message": "wrong password", "code": 400})

@app.route("/api/messages", methods=["GET", "POST"])
@login_required
def api_messages():
    cursor = g.conn.cursor()
    
    if request.method == "GET":
        user1 = request.args.get("user1", type=int)
        user2 = request.args.get("user2", type=int)
        if not user1 or not user2:
            return jsonify({"error": "user1 and user2 required"}), 400
        
        cursor.execute(
            """SELECT * FROM messages 
               WHERE (ownerId = %s AND deliverId = %s) 
                  OR (ownerId = %s AND deliverId = %s)
               ORDER BY id ASC""",
            (user1, user2, user2, user1)
        )
        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows), 200
    
    elif request.method == "POST":
        data = request.json
        owner = data.get("owner")
        deliver = data.get("deliver")
        text = data.get("text")
        
        if not all([owner, deliver, text]):
            return jsonify({"error": "owner, deliver, text required"}), 400
        
        cursor.execute(
            "INSERT INTO messages (ownerId, deliverId, text) VALUES (%s, %s, %s)",
            (owner, deliver, text)
        )
        g.conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"id": new_id, "result": True}), 201
    
@app.route("/send_mes", methods=["POST"])
@login_required
def send_mes():
    data = request.json
    cursor = g.conn.cursor()
    cursor.execute("INSERT INTO messages (ownerId, deliverId, text) VALUES (%s,%s,%s)",
                   (data["owner"], data["deliver"], data["text"]))
    g.conn.commit()
    new_mes_id = cursor.lastrowid
    cursor.close()
    return jsonify({"result": True, "mes_id": new_mes_id, "code": 200})

@app.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    session.pop("user_login", None)
    return redirect('/')
app.run()
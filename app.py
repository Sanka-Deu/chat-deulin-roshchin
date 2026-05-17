from flask import Flask, render_template, request, g
import mysql.connector

app = Flask(__name__)

'''@app.before_request
def connect():
    conn = mysql.connector.connect(
        host="",
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

@app.route("/user_registration", methods=["POST"])
def user_registration():
    #cursor = g.conn.cursor()
    data = request.json
    return "1"

@app.route("/chat")
def chat():
    name = request.args.get("nickname")
    return f"{name}, привет!"

app.run()
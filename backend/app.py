from flask import Flask, render_template, request
import sqlite3
import newdb


app = Flask(__name__)
app.secret_key = "Y76RGT67-èEF676GEeg56"

@app.route("/items")
def index():
    return "Message d'accueil"

def remove_item():



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
from flask import Flask, jsonify, render_template, request
import newdb


app = Flask(__name__)
app.secret_key = "Y76RGT67-èEF676GEeg56"



@app.route("/")
def index():
    return "Message d'accueil"


@app.route("/read_db_table", methods=["GET"])
def read_db_table():
    table = (newdb.read_table())
    return jsonify(table)


@app.route("/insert_db_item", methods=["POST"])
def insert_db_item():
    data = request.get_json()

    name = data["name"]
    batch_number = data["batch_number"]
    initial_quantity = data["initial_quantity"]
    expiration_date = data["expiration_date"]
    form = data["form"]
    dosage = data["dosage"]
    prescription_required = data["prescription_required"]

    newdb.insert_item(name, batch_number, initial_quantity, expiration_date, form, dosage, prescription_required)
    return jsonify({"message": "Item inserted successfully"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
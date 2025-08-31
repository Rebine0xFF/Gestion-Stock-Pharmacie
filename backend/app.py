from flask import Flask, jsonify, render_template, request
import newdb


app = Flask(__name__)
app.secret_key = "Y76RGT67-èEF676GEeg56"



@app.route("/inventory")
def inventory():
    return render_template("inventory.html")

@app.route("/add-product")
def add_product():
    return render_template("add_product.html")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")



@app.route("/read_db_table", methods=["GET"])
def read_db_table():
    table = (newdb.read_table())
    return jsonify(table)


@app.route("/insert_db_item", methods=["POST"])
def insert_db_item():
    data = request.get_json()

    success = newdb.insert_item(
        data["name"],
        data["batch_number"],
        data["initial_quantity"],
        data["expiration_date"],
        data["form"],
        data["dosage"],
        data["prescription_required"]
    )
    if success:
        return jsonify({"message": "Item inserted successfully"}), 201
    else:
        return jsonify({"error": "Batch number already exists"}), 400


@app.route("/subtract_db_item", methods=["POST"])
def subtract_db_item ():
    data = request.get_json()
    batch_number = data["batch_number"]
    newdb.subtract_item(batch_number)
    return jsonify({"message": "Item subtracted successfully"})


@app.route("/remove_db_item", methods=["POST"])
def remove_db_items():
    data = request.get_json()
    batch_number = data["batch_number"]
    newdb.remove_item(batch_number)
    return jsonify({"message": "Item removed successfully"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
from flask import Flask, jsonify, request, render_template, redirect, url_for
from operator import itemgetter
import json

app = Flask(__name__)

# Each transaction will be in a format similar to {"payer": "DANNON", "points": 5000, "timestamp": "2020-11-02T14:00:00Z"}
transactions = []


def return_index_if_payer_exists(payer):
    for index, item in enumerate(transactions):
        if item["payer"] == payer:
            return index
    return -1


def spend_points(points_to_spend):
    # !Untested yet
    transactions_sorted_by_timestamp = sorted(transactions, key=itemgetter("timestamp"))
    index = 0
    while points_to_spend != 0 and index < len(transactions):
        points = transactions_sorted_by_timestamp[index]["points"]
        if points_to_spend < points:
            remainder = points - points_to_spend
        else:
            points_to_spend -= points
            remainder = 0

        transactions_sorted_by_timestamp[index]["points"] = remainder
        index += 1


def add_points(payer, points_to_add, timestamp):
    # !Needs to check if payer exists and add to that

    index = return_index_if_payer_exists(payer)

    if index == -1:
        transactions.append(
            {"payer": payer, "points": points_to_add, "timestamp": timestamp}
        )
    else:
        transactions[index]["points"] += points_to_add


# Define a route for the root URL path
@app.route("/", methods=["GET"])
def welcome():
    return render_template("index.html")


# Route to add transactions
@app.route("/add", methods=["POST"])
def add():
    try:
        data = json.loads(request.form["text"])
        payer = data["payer"]
        points = int(data["points"])
        timestamp = data["timestamp"]

        print("Here")

        add_points(payer, points, timestamp)

        return render_template("index.html"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Route to spend points
@app.route("/spend", methods=["POST"])
def spend():
    try:
        data = json.loads(request.form["text"])

        points = int(data["points"])
        spend_points(points)
        return render_template("index.html"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Route to spend points
@app.route("/balance", methods=["GET"])
def balance():
    return jsonify(transactions), 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)

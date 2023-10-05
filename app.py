from flask import Flask, jsonify, request, render_template, redirect, url_for
from operator import itemgetter
import json

# Each transaction will be in a format similar to {"payer": "DANNON", "points": 5000, "timestamp": "2020-11-02T14:00:00Z"}
transactions = []
total_points = 0

app = Flask(__name__)


def spend_points(points_to_spend):
    global total_points

    total_points -= points_to_spend

    message = []
    transactions_sorted_by_timestamp = sorted(transactions, key=itemgetter("timestamp"))
    index = 0
    while points_to_spend != 0 and index < len(transactions):
        points = transactions_sorted_by_timestamp[index]["points"]
        if points_to_spend < points:
            remainder = points - points_to_spend
        else:
            points_to_spend -= points
            remainder = 0
        payer = transactions_sorted_by_timestamp[index]
        points = -transactions_sorted_by_timestamp[points]
        message.append({"payer": payer, "points": points})

        transactions_sorted_by_timestamp[index]["points"] = remainder
        index += 1


def add_points(payer, points_to_add, timestamp):
    # !Needs to check if payer exists and add to that
    global total_points
    total_points += points_to_add

    transactions.append(
        {"payer": payer, "points": points_to_add, "timestamp": timestamp}
    )


# A route for the root URL path
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

        add_points(payer, points, timestamp)

        return render_template("index.html"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Route to spend points
@app.route("/spend", methods=["POST"])
def spend():
    global total_points
    try:
        data = json.loads(request.form["text"])

        points = int(data["points"])
        if points > total_points:
            message = "You don't have enough points"
            return message, 400
        message = spend_points(points)
        return message, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Route to spend points
@app.route("/balance", methods=["GET"])
def balance():
    return jsonify(transactions), 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)

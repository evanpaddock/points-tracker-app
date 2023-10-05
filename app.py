from flask import Flask, jsonify, request, render_template
from operator import itemgetter
import json
from datetime import datetime

# Each transaction will be in a format similar to {"payer": "DANNON", "points": 5000, "timestamp": "2020-11-02T14:00:00Z"}
transactions = []
total_points = 0

app = Flask(__name__)


def spend_points(points_to_spend):
    global total_points, transactions

    total_points -= points_to_spend

    message = []
    transactions_sorted_by_timestamp = sorted(
        transactions, key=itemgetter("timestamp"), reverse=True
    )
    index = 0
    while points_to_spend != 0 and index < len(transactions):
        payer_points = transactions_sorted_by_timestamp[index]["points"]
        payer = transactions_sorted_by_timestamp[index]["payer"]
        if points_to_spend < payer_points:
            remainder = payer_points - points_to_spend
            points = -transactions_sorted_by_timestamp[index]["points"]
        else:
            points = -points_to_spend
            points_to_spend -= payer_points
            remainder = 0

        message.append({"payer": payer, "points": points})

        transactions_sorted_by_timestamp[index]["points"] = remainder
        transactions = transactions_sorted_by_timestamp
        index += 1

        return message


def add_points(payer, points_to_add, timestamp):
    global total_points
    total_points += points_to_add

    transactions.append(
        {"payer": payer, "points": points_to_add, "timestamp": timestamp}
    )


def get_points_by_payer():
    transactions_by_payers = sorted(transactions, key=itemgetter("payer"))
    points_by_payer = []

    payer = transactions_by_payers[0]["payer"]
    points = transactions_by_payers[0]["points"]
    index = 1

    while index < len(transactions_by_payers):
        if payer == transactions_by_payers[index]["payer"]:
            points += transactions_by_payers[index]["points"]
        else:
            points_by_payer.append({"payer": payer, "points": points})
            payer = transactions_by_payers[index]["payer"]
            points = transactions_by_payers[index]["points"]
        index += 1

    points_by_payer.append({"payer": payer, "points": points})

    return points_by_payer


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
        timestamp = datetime.fromtimestamp(data["timestamp"])

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

        points = data["points"]
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
    message = get_points_by_payer()
    return message, 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)

from flask import Flask, jsonify
from operator import itemgetter
import json

app = Flask(__name__)

# Each transaction will be in a format similar to {"payer": "DANNON", "points": 5000, "timestamp": "2020-11-02T14:00:00Z"}
transactions = []


def spend_points(points_to_spend):
    # !Untested yet
    transactions_sorted_by_timestamp = sorted(transactions, key=itemgetter("timestamp"))
    index = 0
    while points_to_spend != 0 and index <= len(transactions):
        points = transactions_sorted_by_timestamp[index]["points"]
        if points_to_spend < points:
            remainder = points - points_to_spend
        else:
            points_to_spend -= points
            remainder = 0

        transactions_sorted_by_timestamp[index]["points"] = remainder


def add_points(payer, points_to_add, timestamp):
    # !Needs to check if payer exists and add to that
    transactions.append(
        {"payer": payer, "points": points_to_add, "timestamp": timestamp}
    )


def get_balance():
    message = []
    for item in transactions:
        message.append({f"{item['payer']}": {item["points"]}})
    return message


# Define a route for the root URL path
@app.route("/", methods=["GET"])
def welcome():
    return (
        "Welcome to Fetch points tracker. Use /add, /spend, and /balance endpoints.",
        200,
    )


# Route to add transactions
@app.route("/add<json_data>")
def add(json_data):
    try:
        data = json.loads(json_data)
        payer = data["payer"]
        points = data["points"]
        timestamp = data["timestamp"]

        add_points(payer, points, timestamp)

        return "", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Route to spend points
@app.route("/spend<json_data>", methods=["POST"])
def spend(json_data):
    try:
        data = json.loads(json_data)
        points = int(data["points"])
        # !Needs to return a dictionary of payers and points taken off
        message = spend_points(points)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Route to spend points
@app.route("/balance", methods=["GET"])
def balance():
    # !Needs to return a dictionary of payers and total points
    message = get_balance()
    return jsonify(message), 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)

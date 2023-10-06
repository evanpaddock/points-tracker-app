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

    transactions.sort(key=itemgetter("timestamp"))

    message = []

    index = 0

    while points_to_spend != 0:
        current_payer_points = transactions[index]["points"]
        current_payer = transactions[index]["payer"]
        if current_payer_points < points_to_spend:
            # Points for message are equal to the negative of points
            points_spent = -current_payer_points
            # Subtracts current points from points being spent
            points_to_spend -= current_payer_points
            # Remining points = 0 since points being spend > current points
            remainder = 0

        else:
            # All remaining points being spent are used up here so points for message is the opposite of it
            points_spent = -points_to_spend
            # Should equal zero to end loop
            points_to_spend = 0
            # remainder to assign back to payer
            remainder = current_payer_points - points_to_spend

        transactions[index]["points"] = remainder

        message.append({"payer": current_payer, "points": points_spent})

        index += 1

    return message


def add_points(payer, points_to_add, timestamp):
    global total_points
    # Adds new transaction to total points
    total_points += points_to_add

    # adds the new transaction
    transactions.append(
        {"payer": payer, "points": points_to_add, "timestamp": timestamp}
    )


def get_points_by_payer():
    global transactions
    transactions.sort(key=itemgetter("payer"))
    points_by_payer = []

    current_payer = transactions[0]["payer"]
    current_total_points = transactions[0]["points"]
    index = 1

    while index < len(transactions):
        if current_payer == transactions[index]["payer"]:
            current_total_points += transactions[index]["points"]
        else:
            points_by_payer.append(
                {"payer": current_payer, "points": current_total_points}
            )
            current_payer = transactions[index]["payer"]
            current_total_points = transactions[index]["points"]
        index += 1

    points_by_payer.append({"payer": current_payer, "points": current_total_points})

    return points_by_payer


# A route for the root URL path
@app.route("/", methods=["GET"])
def welcome():
    return render_template("index.html")


# Route to add transactions
@app.route("/add", methods=["POST"])
def add():

    # Example Transactions to add
    # { "payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z" }
    # { "payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z" }
    # { "payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z" }
    # { "payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z" }
    # { "payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z" }
    
    try:
        # Gets the data submitted in the add form
        data = json.loads(request.form["data"])

        # gets the different items needed to add a transactions and parses them into the needed format for the system to use.
        payer = data["payer"]
        points = int(data["points"])
        timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%SZ")

        if points > 0:
            add_points(payer, points, timestamp)

        return render_template("index.html"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Route to spend points
@app.route("/spend", methods=["POST"])
def spend():
    global total_points
    try:
        data = json.loads(request.form["data"])

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
    if len(transactions) != 0:
        message = get_points_by_payer()
        return message, 200
    return "You have not added any transactions yet.", 400


if __name__ == "__main__":
    app.run(debug=True, port=8000)

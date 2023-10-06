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
            # Remaining points = 0 since points being spent > current points
            remainder = 0
            # Subtracts current points from points being spent
            points_to_spend -= current_payer_points
        else:
            # All remaining points being spent are used up here so points for message is the opposite of it
            points_spent = -points_to_spend
            # remainder to assign back to payer, points spent is negative
            remainder = current_payer_points + points_spent
            # Set points_to_spend to 0 to end the loop
            points_to_spend = 0

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


def get_points_by_payer(transactions):
    # sorts transactions by the payer field
    transactions.sort(key=itemgetter("payer"))

    # new array to store points spent by payer
    points_by_payer = []

    current_payer = transactions[0]["payer"]
    current_total_points = transactions[0]["points"]

    index = 1

    while index < len(transactions):
        # if same payer as previous, adds to total
        if current_payer == transactions[index]["payer"]:
            current_total_points += transactions[index]["points"]
        # else appends payer and total to points_by_payer array and sets new payer and total points
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
    # Renders index.html file for ease of use
    return render_template("index.html")


# Route to add transactions
@app.route("/add", methods=["POST"])
def add():
    # Example Transactions to add for ease of tester
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

        # Only adds points if points are not negative
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

        # Message of points spent by payer
        message = get_points_by_payer(spend_points(points))

        return message, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Route to spend points
@app.route("/balance", methods=["GET"])
def balance():
    global transactions
    if len(transactions) != 0:
        message = get_points_by_payer(transactions)
        return message, 200
    return "You have not added any transactions yet.", 400


if __name__ == "__main__":
    # runs app on port 8000, debug off
    app.run(port=8000)

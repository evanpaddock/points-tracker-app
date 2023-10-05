from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

transactions = {}


def spend_points(points_to_spend):
    pass


def add_points(points_to_add):
    pass


def get_balance():
    pass


# Route to add transactions
@app.route("/add", methods=["POST"])
def add():
    pass


# Route to spend points
@app.route("/spend", methods=["POST"])
def spend():
    pass


# Route to spend points
@app.route("/balance", methods=["GET"])
def spend():
    pass


if __name__ == "__main__":
    app.run(debug=True, port=8000)

# 🎉 Welcome to the Points Tracker App! 🚀

Track and manage your points with style! This Flask application lets you keep tabs on your earned and spent points by different payers. Let's dive right in!

## 🛠️ Prerequisites

Before you embark on your points-tracking adventure, make sure you have the following tools installed on your trusty computer:

- **Python** (3.x recommended)
- **Flask** (the magic web framework)
- **Git** (optional, but handy for cloning the repository)

## 🚀 Installation

1. **Clone the Repository (or Download the Code)**

   ```terminal
   git clone https://github.com/your-username/points-tracker-app.git
   ```

## 🏃 Running the code

1. **Navigate to the Project Directory**

   ```terminal
   cd points-tracker-app
   ```
2. **Create a Virtual Environment (Highly Recommended)**

   ```terminal
   python -m venv venv
   ```
3. **Activate the Virtual Environment**

   On Windows:
    ```terminal
    venv\Scripts\activate
    ```

    On macOS and Linux:
    ```terminal
    source venv/bin/activate
    ```
4. **Install the Required Python Packages**

   On Windows:
    ```terminal
    venv\Scripts\activate
    ```

    On macOS and Linux:
    ```terminal
    source venv/bin/activate
    ```
Install the Required Python Packages
bash
Copy code
pip install -r requirements.txt
🎮 Usage
Start the Flask Application

bash
Copy code
python app.py
Your application will be up and running at http://127.0.0.1:8000/.

Access the Web Interface

Fire up your favorite web browser and navigate to http://127.0.0.1:8000/ to unlock the points-tracking magic!

Routes at Your Fingertips

/add (POST): Add transactions.
/spend (POST): Spend points from your balance.
/balance (GET): Check your point balance by payer.
💰 Adding Transactions
To add transactions, use the /add route with this friendly JSON format:

json
Copy code
{
"payer": "DANNON",
"points": 300,
"timestamp": "2022-10-31T10:00:00Z"
}
Customize the values with the payer's name, points, and timestamp to your heart's content.

💸 Spending Points
To spend points, visit the /spend route and send a JSON request like this:

json
Copy code
{
"points": 500
}
Just replace 500 with the number of points you're ready to splurge. Make sure you've got enough points in your balance!

🧮 Checking Point Balance
Wondering how many points you have left? Simply hit the /balance route to see your point balance by payer.

👥 Contributing
We'd love to have you on board! Feel free to contribute to this project by creating pull requests or reporting issues. Let's make points-tracking even more fun!

📜 License
This project is licensed under the MIT License. For all the nitty-gritty details, check out the LICENSE file.

Happy points tracking! 🎈

# 🎉 Welcome to the Points Tracker App! 🚀

Track and manage your points with style! This Flask application lets you keep tabs on your earned and spent points by different payers. Let's dive right in!

## 🛠️ Prerequisites

Before you embark on your points-tracking adventure, make sure you have the following tools installed on your trusty computer:

- **Python** (3.x recommended)
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

   ```terminal
   pip install -r requirements.txt
   ```

## 🎮 Usage

1. **Start the Flask Application**

   ```terminal
   python app.py
   ```

   The application will run on http://127.0.0.1:8000/ by default.

2. **Access the Web Interface**

   Open a web browser and navigate to http://127.0.0.1:8000/ to access the application.

## Routes

1. **/add (POST): Add transactions.**

2. **/spend (POST): Spend points from the balance.**

3. **/balance (GET): Check the point balance by payer.**

Happy points tracking! 🎈

from flask import Flask, render_template, request, session, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

def weather_description(code):

    if code == 0:
        return "Clear sky"

    elif code in [1, 2, 3]:
        return "Cloudy"

    elif code in [45, 48]:
        return "Fog"

    elif code in [51, 53, 55, 61, 63, 65]:
        return "Rain"

    elif code in [71, 73, 75]:
        return "Snow"

    elif code in [80, 81, 82]:
        return "Rain showers"

    elif code in [95, 96, 99]:
        return "Thunderstorm"

    else:
        return "Unknown"

def init_db():

    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nickname TEXT UNIQUE NOT NULL,
            score INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            correct_answer TEXT NOT NULL
        )
    """)

    cursor.execute("""
        SELECT COUNT(*) FROM questions
    """)

    question_count = cursor.fetchone()[0]

    if question_count == 0:

        cursor.execute("""
            INSERT INTO questions
            (question, option1, option2, option3, option4, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Which Python library is commonly used for machine learning?",
            "Flask",
            "scikit-learn",
            "SQLite",
            "Bootstrap",
            "scikit-learn"
        ))

        cursor.execute("""
            INSERT INTO questions
            (question, option1, option2, option3, option4, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Which keyword is used to define a function in Python?",
            "func",
            "define",
            "def",
            "function",
            "def"
        ))

        cursor.execute("""
            INSERT INTO questions
            (question, option1, option2, option3, option4, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Which of these is a Python web framework?",
            "Flask",
            "NumPy",
            "Pandas",
            "Matplotlib",
            "Flask"
        ))

    connection.commit()
    connection.close()

@app.route("/", methods=["GET", "POST"])
def home():

    username = session.get("username")

    weather_data = None

    if request.method == "POST":

        city = request.form.get("city")

        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

        geocoding_params = {
            "name": city,
            "count": 1
        }

        geocoding_response = requests.get(
            geocoding_url,
            params=geocoding_params
        )

        geocoding_data = geocoding_response.json()

        if "results" in geocoding_data:

            location = geocoding_data["results"][0]

            latitude = location["latitude"]
            longitude = location["longitude"]

            forecast_url = "https://api.open-meteo.com/v1/forecast"

            forecast_params = {
                "latitude": latitude,
                "longitude": longitude,
                "daily": "temperature_2m_max,temperature_2m_min,weather_code",
                "forecast_days": 3,
                "timezone": "auto"
            }

            forecast_response = requests.get(
                forecast_url,
                params=forecast_params
            )

            weather_data = forecast_response.json()

            for date in weather_data["daily"]["time"]:
                weekday = datetime.strptime(date, "%Y-%m-%d").strftime("%A")

                if "weekdays" not in weather_data:
                    weather_data["weekdays"] = []

                weather_data["weekdays"].append(weekday)
            
            weather_data["descriptions"] = []

            for code in weather_data["daily"]["weather_code"]:

                description = weather_description(code)

                weather_data["descriptions"].append(description)

            print(weather_data)

    return render_template(
        "home.html",
        username=username,
        weather_data=weather_data
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()

        connection.close()

        if user is None:
            message = "User not found"

        else:
            stored_password = user[2]

            if check_password_hash(stored_password, password):
                session["user_id"] = user[0]
                session["username"] = user[1]
                session["nickname"] = user[3]

                message = "Login successful"
            else:
                message = "Wrong password"

    return render_template(
        "login.html",
        message=message
    )

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        print(username)
        print(password)

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        nickname = request.form["nickname"]

        if password != confirm_password:
            message = "Passwords do not match"

        else:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            try:
                hashed_password = generate_password_hash(password)

                cursor.execute("""
                    INSERT INTO users (username, password, nickname)
                    VALUES (?, ?, ?)
                """, (username, hashed_password, nickname))

                connection.commit()
                message = "Registration successful"

            except sqlite3.IntegrityError:
                message = "Username or nickname already exists"

            finally:
                connection.close()

    return render_template(
        "register.html",
        message=message
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if "user_id" not in session:
        return redirect("/login")

    message = ""

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    user_id = session["user_id"]

    cursor.execute("""
        SELECT score
        FROM users
        WHERE id = ?
    """, (user_id,))

    score = cursor.fetchone()[0]

    cursor.execute("""
        SELECT *
        FROM questions
        ORDER BY RANDOM()
        LIMIT 1
    """)

    question = cursor.fetchone()

    if request.method == "POST":

        answer = request.form.get("answer")
        question_id = request.form.get("question_id")

        cursor.execute("""
            SELECT correct_answer
            FROM questions
            WHERE id = ?
        """, (question_id,))

        correct_answer = cursor.fetchone()[0]

        if answer == correct_answer:

            cursor.execute("""
                UPDATE users
                SET score = score + 10
                WHERE id = ?
            """, (user_id,))

            connection.commit()

            score += 10

            message = "Correct! +10 points"

        else:
            message = "Wrong answer!"

    connection.close()

    return render_template(
        "quiz.html",
        question=question,
        message=message,
        score=score
    )

@app.route("/ranking")
def ranking():

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT nickname, score
        FROM users
        ORDER BY score DESC
    """)

    users = cursor.fetchall()

    connection.close()

    return render_template(
        "ranking.html",
        users=users
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

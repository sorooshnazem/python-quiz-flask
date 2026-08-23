from flask import Flask, render_template, request, session, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

def init_db():

    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nickname TEXT UNIQUE NOT NULL,
            score INTEGER DEFAULT 0,
            role TEXT NOT NULL DEFAULT 'user'
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

@app.route("/")
def home():

    username = session.get("username")

    return render_template(
        "home.html",
        username=username
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
                session["role"] = user[5]

                print("SESSION AFTER LOGIN:", dict(session))

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


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return "Access denied", 403

    message = ""

    if request.method == "POST":

        question = request.form.get("question")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_answer")

        options = {
            "1": option1,
            "2": option2,
            "3": option3,
            "4": option4
        }

        correct_answer = options.get(correct_option)

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO questions
            (
                question,
                option1,
                option2,
                option3,
                option4,
                correct_answer
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            question,
            option1,
            option2,
            option3,
            option4,
            correct_answer
        ))

        connection.commit()
        connection.close()

        message = "Domanda aggiunta con successo!"

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            question,
            option1,
            option2,
            option3,
            option4,
            correct_answer
        FROM questions
        ORDER BY id DESC
    """)

    questions = cursor.fetchall()

    connection.close()

    return render_template(
        "admin.html",
        message=message,
        questions=questions
    )

@app.route("/admin/delete/<int:question_id>", methods=["POST"])
def delete_question(question_id):

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return "Access denied", 403

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM questions
        WHERE id = ?
    """, (question_id,))

    connection.commit()
    connection.close()

    return redirect("/admin")

@app.route(
    "/admin/edit/<int:question_id>",
    methods=["GET", "POST"]
)
def edit_question(question_id):

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return "Access denied", 403

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    if request.method == "POST":

        question_text = request.form.get("question")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_answer")

        options = {
            "1": option1,
            "2": option2,
            "3": option3,
            "4": option4
        }

        correct_answer = options.get(correct_option)

        cursor.execute("""
            UPDATE questions
            SET
                question = ?,
                option1 = ?,
                option2 = ?,
                option3 = ?,
                option4 = ?,
                correct_answer = ?
            WHERE id = ?
        """, (
            question_text,
            option1,
            option2,
            option3,
            option4,
            correct_answer,
            question_id
        ))

        connection.commit()
        connection.close()

        return redirect("/admin")

    cursor.execute("""
        SELECT
            id,
            question,
            option1,
            option2,
            option3,
            option4,
            correct_answer
        FROM questions
        WHERE id = ?
    """, (question_id,))

    question = cursor.fetchone()

    connection.close()

    if question is None:
        return "Question not found", 404

    return render_template(
        "edit_question.html",
        question=question
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

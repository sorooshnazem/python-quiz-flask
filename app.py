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
            correct_answer TEXT NOT NULL,
            course_id INTEGER,
            topic_id INTEGER,
            difficulty TEXT NOT NULL DEFAULT 'Beginner',
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (topic_id) REFERENCES topics(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO courses (name)
        VALUES (?)
    """, ("Python",))

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)

    cursor.execute("""
        SELECT id
        FROM courses
        WHERE name = ?
    """, ("Python",))

    python_course = cursor.fetchone()

    if python_course:

        python_course_id = python_course[0]

        topics = [
            "Basics",
            "Data Types",
            "Control Flow",
            "Functions",
            "OOP",
            "Exceptions"
        ]

        for topic in topics:

            cursor.execute("""
                SELECT id
                FROM topics
                WHERE name = ?
                AND course_id = ?
            """, (
                topic,
                python_course_id
            ))

            existing_topic = cursor.fetchone()

            if existing_topic is None:

                cursor.execute("""
                    INSERT INTO topics (name, course_id)
                    VALUES (?, ?)
                """, (
                    topic,
                    python_course_id
                ))

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

    # -----------------------------------
    # RECUPERA TOPIC E DIFFICULTY
    # -----------------------------------

    if request.method == "POST":
        selected_topic = request.form.get("topic")
        selected_difficulty = request.form.get("difficulty")
    else:
        selected_topic = request.args.get("topic")
        selected_difficulty = request.args.get("difficulty")

    if selected_topic in ("", "None", None):
        selected_topic = None

    if selected_difficulty in ("", "None", None):
        selected_difficulty = None

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    user_id = session["user_id"]

    # -----------------------------------
    # RECUPERA IL PUNTEGGIO
    # -----------------------------------

    cursor.execute("""
        SELECT score
        FROM users
        WHERE id = ?
    """, (user_id,))

    score = cursor.fetchone()[0]

    # -----------------------------------
    # RECUPERA ID CORSO PYTHON
    # -----------------------------------

    cursor.execute("""
        SELECT id
        FROM courses
        WHERE name = ?
    """, ("Python",))

    course = cursor.fetchone()

    if course is None:
        connection.close()
        return "Python course not found", 404

    course_id = course[0]

    # -----------------------------------
    # SE L'UTENTE HA RISPOSTO
    # CONTROLLA PRIMA LA RISPOSTA
    # -----------------------------------

    if request.method == "POST":

        answer = request.form.get("answer")
        question_id = request.form.get("question_id")

        cursor.execute("""
            SELECT correct_answer
            FROM questions
            WHERE id = ?
            AND course_id = ?
        """, (
            question_id,
            course_id
        ))

        result = cursor.fetchone()

        if result is None:
            connection.close()
            return "Question not found", 404

        correct_answer = result[0]

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

    # -----------------------------------
    # ORA RECUPERA LA PROSSIMA DOMANDA
    # -----------------------------------

    if selected_topic and selected_difficulty:

        cursor.execute("""
            SELECT *
            FROM questions
            WHERE course_id = ?
            AND topic_id = ?
            AND difficulty = ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (
            course_id,
            selected_topic,
            selected_difficulty
        ))

    elif selected_topic:

        cursor.execute("""
            SELECT *
            FROM questions
            WHERE course_id = ?
            AND topic_id = ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (
            course_id,
            selected_topic
        ))

    else:

        cursor.execute("""
            SELECT *
            FROM questions
            WHERE course_id = ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (course_id,))

    question = cursor.fetchone()

    if question is None:
        connection.close()
        return "No questions available for this topic and difficulty", 404

    connection.close()

    return render_template(
        "quiz.html",
        question=question,
        message=message,
        score=score,
        selected_topic=selected_topic,
        selected_difficulty=selected_difficulty
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

    selected_topic = request.args.get("topic")
    selected_difficulty = request.args.get("difficulty")

    # -----------------------------------
    # AGGIUNTA DI UNA NUOVA DOMANDA
    # -----------------------------------

    if request.method == "POST":

        question = request.form.get("question")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        topic_id = request.form.get("topic_id")
        difficulty = request.form.get("difficulty")
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

        # Recupera l'id del corso Python
        cursor.execute("""
            SELECT id
            FROM courses
            WHERE name = ?
        """, ("Python",))

        course = cursor.fetchone()

        if course is None:
            connection.close()
            return "Python course not found", 404

        course_id = course[0]

        # Inserisce la nuova domanda
        cursor.execute("""
            INSERT INTO questions
            (
                question,
                option1,
                option2,
                option3,
                option4,
                correct_answer,
                course_id,
                topic_id,
                difficulty
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            question,
            option1,
            option2,
            option3,
            option4,
            correct_answer,
            course_id,
            topic_id,
            difficulty
        ))

        connection.commit()
        connection.close()

        message = "Domanda aggiunta con successo!"

    # -----------------------------------
    # RECUPERA I TOPIC PYTHON
    # -----------------------------------

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            topics.id,
            topics.name
        FROM topics
        JOIN courses
            ON topics.course_id = courses.id
        WHERE courses.name = ?
        ORDER BY topics.name
    """, ("Python",))

    topics = cursor.fetchall()

    # -----------------------------------
    # RECUPERA LE DOMANDE
    # CON FILTRO TOPIC + DIFFICULTY
    # -----------------------------------

    if selected_topic and selected_difficulty:

        cursor.execute("""
            SELECT
                questions.id,
                questions.question,
                questions.option1,
                questions.option2,
                questions.option3,
                questions.option4,
                questions.correct_answer,
                topics.name,
                questions.difficulty
            FROM questions
            LEFT JOIN topics
                ON questions.topic_id = topics.id
            JOIN courses
                ON questions.course_id = courses.id
            WHERE courses.name = ?
            AND questions.topic_id = ?
            AND questions.difficulty = ?
            ORDER BY questions.id DESC
        """, (
            "Python",
            selected_topic,
            selected_difficulty
        ))

    elif selected_topic:

        cursor.execute("""
            SELECT
                questions.id,
                questions.question,
                questions.option1,
                questions.option2,
                questions.option3,
                questions.option4,
                questions.correct_answer,
                topics.name,
                questions.difficulty
            FROM questions
            LEFT JOIN topics
                ON questions.topic_id = topics.id
            JOIN courses
                ON questions.course_id = courses.id
            WHERE courses.name = ?
            AND questions.topic_id = ?
            ORDER BY questions.id DESC
        """, (
            "Python",
            selected_topic
        ))

    elif selected_difficulty:

        cursor.execute("""
            SELECT
                questions.id,
                questions.question,
                questions.option1,
                questions.option2,
                questions.option3,
                questions.option4,
                questions.correct_answer,
                topics.name,
                questions.difficulty
            FROM questions
            LEFT JOIN topics
                ON questions.topic_id = topics.id
            JOIN courses
                ON questions.course_id = courses.id
            WHERE courses.name = ?
            AND questions.difficulty = ?
            ORDER BY questions.id DESC
        """, (
            "Python",
            selected_difficulty
        ))

    else:

        cursor.execute("""
            SELECT
                questions.id,
                questions.question,
                questions.option1,
                questions.option2,
                questions.option3,
                questions.option4,
                questions.correct_answer,
                topics.name,
                questions.difficulty
            FROM questions
            LEFT JOIN topics
                ON questions.topic_id = topics.id
            JOIN courses
                ON questions.course_id = courses.id
            WHERE courses.name = ?
            ORDER BY questions.id DESC
        """, ("Python",))

    questions = cursor.fetchall()

    connection.close()

    return render_template(
        "admin.html",
        message=message,
        questions=questions,
        topics=topics,
        selected_topic=selected_topic,
        selected_difficulty=selected_difficulty
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
        topic_id = request.form.get("topic_id")
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
                correct_answer = ?,
                topic_id = ?
            WHERE id = ?
        """, (
            question_text,
            option1,
            option2,
            option3,
            option4,
            correct_answer,
            topic_id,
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
            correct_answer,
            topic_id,
            difficulty
        FROM questions
        WHERE id = ?
    """, (question_id,))

    question = cursor.fetchone()

    if question is None:
        connection.close()
        return "Question not found", 404

    cursor.execute("""
        SELECT topics.id, topics.name
        FROM topics
        JOIN courses
            ON topics.course_id = courses.id
        WHERE courses.name = ?
        ORDER BY topics.name
    """, ("Python",))

    topics = cursor.fetchall()

    connection.close()

    return render_template(
        "edit_question.html",
        question=question,
        topics=topics
    )

@app.route("/quiz/topics")
def quiz_topics():

    if "user_id" not in session:
        return redirect("/login")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            topics.id,
            topics.name
        FROM topics
        JOIN courses
            ON topics.course_id = courses.id
        WHERE courses.name = ?
        ORDER BY topics.name
    """, ("Python",))

    topics = cursor.fetchall()

    connection.close()

    return render_template(
        "quiz_topics.html",
        topics=topics
    )

@app.route("/quiz/difficulty")
def quiz_difficulty():

    if "user_id" not in session:
        return redirect("/login")

    selected_topic = request.args.get("topic")

    if not selected_topic:
        return redirect("/quiz/topics")

    return render_template(
        "quiz_difficulty.html",
        selected_topic=selected_topic
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

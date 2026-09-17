from flask import Flask, render_template, request, session, redirect
import sqlite3
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps
from dotenv import load_dotenv
from init_db import init_db
from seed_data import seed_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "SECRET_KEY environment variable is not configured"
    )

def admin_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:
            return redirect("/login")

        if session.get("role") != "admin":
            return "Access denied", 403

        return function(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():

    username = session.get("username")

    return render_template(
        "home.html",
        username=username
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    # Se l'utente è già autenticato,
    # non ha bisogno di vedere nuovamente il login.
    if "user_id" in session:
        return redirect("/")

    message = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # ---------------------------------------------------------
        # BASIC VALIDATION
        # ---------------------------------------------------------

        if not username or not password:

            message = "Username and password are required"

            return render_template(
                "login.html",
                message=message
            )

        # ---------------------------------------------------------
        # FIND USER
        # ---------------------------------------------------------

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                username,
                password,
                nickname,
                score,
                role
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        connection.close()

        # ---------------------------------------------------------
        # CHECK CREDENTIALS
        # ---------------------------------------------------------

        if user is None:

            message = "Invalid username or password"

        else:

            stored_password = user[2]

            if check_password_hash(
                stored_password,
                password
            ):

                # Pulisce eventuali dati rimasti
                # da una sessione precedente.
                session.clear()

                session["user_id"] = user[0]
                session["username"] = user[1]
                session["nickname"] = user[3]
                session["role"] = user[5]

                return redirect("/")

            else:

                message = "Invalid username or password"

    # ---------------------------------------------------------
    # SHOW LOGIN PAGE
    # ---------------------------------------------------------

    return render_template(
        "login.html",
        message=message
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    # Se l'utente è già autenticato,
    # non deve registrare un nuovo account.
    if "user_id" in session:
        return redirect("/")

    message = ""

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        nickname = request.form.get(
            "nickname",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        # ---------------------------------------------------------
        # 1. REQUIRED FIELDS
        # ---------------------------------------------------------

        if (
            not username
            or not nickname
            or not password
            or not confirm_password
        ):

            message = "All fields are required"

            return render_template(
                "register.html",
                message=message
            )

        # ---------------------------------------------------------
        # 2. USERNAME LENGTH
        # ---------------------------------------------------------

        if len(username) < 3:

            message = (
                "Username must contain "
                "at least 3 characters"
            )

            return render_template(
                "register.html",
                message=message
            )

        # ---------------------------------------------------------
        # 3. NICKNAME LENGTH
        # ---------------------------------------------------------

        if len(nickname) < 2:

            message = (
                "Nickname must contain "
                "at least 2 characters"
            )

            return render_template(
                "register.html",
                message=message
            )

        # ---------------------------------------------------------
        # 4. PASSWORD LENGTH
        # ---------------------------------------------------------

        if len(password) < 8:

            message = (
                "Password must contain "
                "at least 8 characters"
            )

            return render_template(
                "register.html",
                message=message
            )

        # ---------------------------------------------------------
        # 5. PASSWORD CONFIRMATION
        # ---------------------------------------------------------

        if password != confirm_password:

            message = "Passwords do not match"

            return render_template(
                "register.html",
                message=message
            )

        # ---------------------------------------------------------
        # 6. DATABASE
        # ---------------------------------------------------------

        connection = get_db_connection()
        cursor = connection.cursor()

        try:

            hashed_password = generate_password_hash(
                password
            )

            cursor.execute("""
                INSERT INTO users (
                    username,
                    password,
                    nickname
                )
                VALUES (?, ?, ?)
            """, (
                username,
                hashed_password,
                nickname
            ))

            connection.commit()

        except sqlite3.IntegrityError:

            connection.close()

            message = (
                "Username or nickname already exists"
            )

            return render_template(
                "register.html",
                message=message
            )

        connection.close()

        # ---------------------------------------------------------
        # 7. REGISTRATION SUCCESSFUL
        # ---------------------------------------------------------

        return redirect("/login")

    # ---------------------------------------------------------
    # SHOW REGISTER PAGE
    # ---------------------------------------------------------

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

    connection = get_db_connection()
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

    user = cursor.fetchone()

    if user is None:
        connection.close()
        return "User not found", 404

    score = user[0]

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

    # =========================================================
    # POST
    # L'UTENTE HA RISPOSTO A UNA DOMANDA
    # =========================================================

    if request.method == "POST":

        answer = request.form.get("answer")
        question_id = request.form.get("question_id")

        # Recuperiamo la stessa domanda
        cursor.execute("""
            SELECT *
            FROM questions
            WHERE id = ?
            AND course_id = ?
        """, (
            question_id,
            course_id
        ))

        question = cursor.fetchone()

        if question is None:
            connection.close()
            return "Question not found", 404

        # correct_answer si trova nella colonna 6
        correct_answer = question[6]

        # -----------------------------------
        # CONTROLLA RISPOSTA
        # -----------------------------------

        if answer == correct_answer:

            rewarded_question_id = session.get(
                "rewarded_question_id"
            )

            if str(rewarded_question_id) != str(question_id):

                cursor.execute("""
                    UPDATE users
                    SET score = score + 10
                    WHERE id = ?
                """, (user_id,))

                connection.commit()

                score += 10

                session["rewarded_question_id"] = question_id

                message = "Correct! +10 points"

            else:

                message = "Correct!"

            is_correct = True

        else:

            is_correct = False
            message = "Wrong answer!"

        connection.close()

        # IMPORTANTE:
        # mostriamo ancora la STESSA domanda,
        # ma in modalità risultato.

        return render_template(
            "quiz.html",
            question=question,
            message=message,
            score=score,
            selected_topic=selected_topic,
            selected_difficulty=selected_difficulty,
            answered=True,
            selected_answer=answer,
            correct_answer=correct_answer,
            is_correct=is_correct
        )

    # =========================================================
    # GET
    # RECUPERA UNA NUOVA DOMANDA
    # =========================================================

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

    elif selected_difficulty:

        cursor.execute("""
            SELECT *
            FROM questions
            WHERE course_id = ?
            AND difficulty = ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (
            course_id,
            selected_difficulty
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

        return render_template(
            "quiz_empty.html",
            selected_topic=selected_topic,
            selected_difficulty=selected_difficulty
        )

    connection.close()

    # -----------------------------------
    # MOSTRA NUOVA DOMANDA
    # -----------------------------------

    return render_template(
        "quiz.html",
        question=question,
        message="",
        score=score,
        selected_topic=selected_topic,
        selected_difficulty=selected_difficulty,
        answered=False,
        selected_answer=None,
        correct_answer=None,
        is_correct=None
    )

@app.route("/ranking")
def ranking():

    connection = get_db_connection()
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
@admin_required
def admin():

    message = ""

    selected_topic = request.args.get("topic")
    selected_difficulty = request.args.get("difficulty")

    # -----------------------------------
    # AGGIUNTA DI UNA NUOVA DOMANDA
    # -----------------------------------

    if request.method == "POST":

        # ---------------------------------------------------------
        # RECUPERA E PULISCE I DATI
        # ---------------------------------------------------------

        question = request.form.get(
            "question",
            ""
        ).strip()

        option1 = request.form.get(
            "option1",
            ""
        ).strip()

        option2 = request.form.get(
            "option2",
            ""
        ).strip()

        option3 = request.form.get(
            "option3",
            ""
        ).strip()

        option4 = request.form.get(
            "option4",
            ""
        ).strip()

        topic_id = request.form.get(
            "topic_id",
            ""
        ).strip()

        difficulty = request.form.get(
            "difficulty",
            ""
        ).strip()

        correct_option = request.form.get(
            "correct_answer",
            ""
        ).strip()

        # ---------------------------------------------------------
        # VALIDAZIONE CAMPI OBBLIGATORI
        # ---------------------------------------------------------

        if not all([
            question,
            option1,
            option2,
            option3,
            option4,
            topic_id,
            difficulty,
            correct_option
        ]):

            message = "Tutti i campi sono obbligatori."

        # ---------------------------------------------------------
        # VALIDAZIONE RISPOSTA CORRETTA
        # ---------------------------------------------------------

        elif correct_option not in ("1", "2", "3", "4"):

            message = "Seleziona una risposta corretta valida."

        # ---------------------------------------------------------
        # VALIDAZIONE DIFFICULTY
        # ---------------------------------------------------------

        elif difficulty not in (
            "Beginner",
            "Intermediate",
            "Advanced"
        ):

            message = "Difficulty non valida."

        # ---------------------------------------------------------
        # VALIDAZIONE TOPIC ID
        # ---------------------------------------------------------

        elif not topic_id.isdigit():

            message = "Topic non valido."

        else:

            options = {
                "1": option1,
                "2": option2,
                "3": option3,
                "4": option4
            }

            correct_answer = options[correct_option]

            connection = get_db_connection()
            cursor = connection.cursor()

            # -----------------------------------------------------
            # RECUPERA IL CORSO PYTHON
            # -----------------------------------------------------

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

            # -----------------------------------------------------
            # VERIFICA CHE IL TOPIC APPARTENGA A PYTHON
            # -----------------------------------------------------

            cursor.execute("""
                SELECT id
                FROM topics
                WHERE id = ?
                AND course_id = ?
            """, (
                topic_id,
                course_id
            ))

            topic = cursor.fetchone()

            if topic is None:

                connection.close()

                message = (
                    "Il topic selezionato non è valido "
                    "per il corso Python."
                )

            else:

                # -------------------------------------------------
                # INSERISCE LA DOMANDA
                # -------------------------------------------------

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

    connection = get_db_connection()
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
@admin_required
def delete_question(question_id):

    connection = get_db_connection()
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
@admin_required
def edit_question(question_id):

    connection = get_db_connection()
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

    connection = get_db_connection()
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

@app.route("/lessons")
def lessons():

    '''
    if "user_id" not in session:
            return redirect("/login")
    '''

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            lessons.id,
            lessons.title,
            lessons.lesson_order,
            topics.name
        FROM lessons
        JOIN topics
            ON lessons.topic_id = topics.id
        ORDER BY
            topics.name,
            lessons.lesson_order
    """)

    lessons = cursor.fetchall()

    connection.close()

    lessons_by_topic = {}

    for lesson in lessons:

        topic_name = lesson[3]

        if topic_name not in lessons_by_topic:
            lessons_by_topic[topic_name] = []

        lessons_by_topic[topic_name].append(lesson)

    return render_template(
        "lessons.html",
        lessons_by_topic=lessons_by_topic
    )

@app.route("/lessons/<int:lesson_id>")
def lesson_detail(lesson_id):

    '''
    if "user_id" not in session:
        return redirect("/login")
    '''

    connection = get_db_connection()
    cursor = connection.cursor()

    # ---------------------------------------------------------
    # GET CURRENT LESSON
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT
            lessons.id,
            lessons.title,
            lessons.lesson_order,
            topics.name,
            topics.id
        FROM lessons
        JOIN topics
            ON lessons.topic_id = topics.id
        WHERE lessons.id = ?
    """, (lesson_id,))

    lesson = cursor.fetchone()

    # ---------------------------------------------------------
    # CHECK IF LESSON EXISTS
    # ---------------------------------------------------------

    if lesson is None:
        connection.close()
        return "Lesson not found", 404

    # ---------------------------------------------------------
    # GET PREVIOUS LESSON
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT
            id,
            title
        FROM lessons
        WHERE topic_id = ?
        AND lesson_order < ?
        ORDER BY lesson_order DESC
        LIMIT 1
    """, (
        lesson[4],
        lesson[2]
    ))

    previous_lesson = cursor.fetchone()

    # ---------------------------------------------------------
    # GET NEXT LESSON
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT
            id,
            title
        FROM lessons
        WHERE topic_id = ?
        AND lesson_order > ?
        ORDER BY lesson_order ASC
        LIMIT 1
    """, (
        lesson[4],
        lesson[2]
    ))

    next_lesson = cursor.fetchone()

    # ---------------------------------------------------------
    # GET LESSON BLOCKS
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT
            block_type,
            content,
            block_order
        FROM lesson_blocks
        WHERE lesson_id = ?
        ORDER BY block_order
    """, (lesson_id,))

    blocks = cursor.fetchall()

    connection.close()

    # ---------------------------------------------------------
    # SHOW LESSON
    # ---------------------------------------------------------

    return render_template(
        "lesson_detail.html",
        lesson=lesson,
        blocks=blocks,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson
    )

@app.route("/admin/lessons")
@admin_required
def admin_lessons():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            lessons.id,
            lessons.lesson_order,
            lessons.title,
            topics.name
        FROM lessons
        JOIN topics
            ON lessons.topic_id = topics.id
        ORDER BY
            topics.name,
            lessons.lesson_order
    """)

    lessons = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_lessons.html",
        lessons=lessons
    )

@app.route("/admin/lessons/add", methods=["GET", "POST"])
@admin_required
def admin_add_lesson():

    connection = get_db_connection()
    cursor = connection.cursor()

    # ---------------------------------------------------------
    # GET PYTHON COURSE
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # GET PYTHON TOPICS
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT
            id,
            name
        FROM topics
        WHERE course_id = ?
        ORDER BY name
    """, (course_id,))

    topics = cursor.fetchall()

    # ---------------------------------------------------------
    # CREATE LESSON
    # ---------------------------------------------------------

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        topic_id = request.form.get(
            "topic_id",
            ""
        ).strip()

        lesson_order = request.form.get(
            "lesson_order",
            ""
        ).strip()

        # -----------------------------------------------------
        # REQUIRED FIELDS
        # -----------------------------------------------------

        if not title or not topic_id or not lesson_order:

            connection.close()

            return render_template(
                "admin_add_lesson.html",
                topics=topics,
                error="Tutti i campi sono obbligatori."
            )

        # -----------------------------------------------------
        # VALIDATE IDs / ORDER
        # -----------------------------------------------------

        if not topic_id.isdigit():

            connection.close()

            return render_template(
                "admin_add_lesson.html",
                topics=topics,
                error="Topic non valido."
            )

        if not lesson_order.isdigit() or int(lesson_order) < 1:

            connection.close()

            return render_template(
                "admin_add_lesson.html",
                topics=topics,
                error="Lesson order deve essere un numero positivo."
            )

        topic_id = int(topic_id)
        lesson_order = int(lesson_order)

        # -----------------------------------------------------
        # CHECK TOPIC
        # -----------------------------------------------------

        cursor.execute("""
            SELECT id
            FROM topics
            WHERE id = ?
            AND course_id = ?
        """, (
            topic_id,
            course_id
        ))

        topic = cursor.fetchone()

        if topic is None:

            connection.close()

            return render_template(
                "admin_add_lesson.html",
                topics=topics,
                error="Il topic selezionato non è valido."
            )

        # -----------------------------------------------------
        # CHECK LESSON ORDER
        # -----------------------------------------------------

        cursor.execute("""
            SELECT id
            FROM lessons
            WHERE topic_id = ?
            AND lesson_order = ?
        """, (
            topic_id,
            lesson_order
        ))

        existing_lesson = cursor.fetchone()

        if existing_lesson is not None:

            connection.close()

            return render_template(
                "admin_add_lesson.html",
                topics=topics,
                error=(
                    "Esiste già una lezione con questo "
                    "ordine nel topic selezionato."
                )
            )

        # -----------------------------------------------------
        # INSERT LESSON
        # -----------------------------------------------------

        cursor.execute("""
            INSERT INTO lessons (
                title,
                topic_id,
                lesson_order
            )
            VALUES (?, ?, ?)
        """, (
            title,
            topic_id,
            lesson_order
        ))

        connection.commit()
        connection.close()

        return redirect("/admin/lessons")

    connection.close()

    return render_template(
        "admin_add_lesson.html",
        topics=topics
    )

@app.route("/admin/lessons/edit/<int:lesson_id>", methods=["GET", "POST"])
@admin_required
def admin_edit_lesson(lesson_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    # ---------------------------------------------------------
    # GET PYTHON COURSE
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # GET LESSON
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT
            lessons.id,
            lessons.title,
            lessons.topic_id,
            lessons.lesson_order
        FROM lessons
        JOIN topics
            ON lessons.topic_id = topics.id
        WHERE lessons.id = ?
        AND topics.course_id = ?
    """, (
        lesson_id,
        course_id
    ))

    lesson = cursor.fetchone()

    if lesson is None:
        connection.close()
        return "Lesson not found", 404

    # ---------------------------------------------------------
    # GET PYTHON TOPICS
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT
            id,
            name
        FROM topics
        WHERE course_id = ?
        ORDER BY name
    """, (course_id,))

    topics = cursor.fetchall()

    # ---------------------------------------------------------
    # UPDATE LESSON
    # ---------------------------------------------------------

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        topic_id = request.form.get(
            "topic_id",
            ""
        ).strip()

        lesson_order = request.form.get(
            "lesson_order",
            ""
        ).strip()

        # -----------------------------------------------------
        # REQUIRED FIELDS
        # -----------------------------------------------------

        if not title or not topic_id or not lesson_order:

            connection.close()

            return render_template(
                "admin_edit_lesson.html",
                lesson=lesson,
                topics=topics,
                error="Tutti i campi sono obbligatori."
            )

        # -----------------------------------------------------
        # VALIDATE TOPIC ID
        # -----------------------------------------------------

        if not topic_id.isdigit():

            connection.close()

            return render_template(
                "admin_edit_lesson.html",
                lesson=lesson,
                topics=topics,
                error="Topic non valido."
            )

        # -----------------------------------------------------
        # VALIDATE LESSON ORDER
        # -----------------------------------------------------

        if not lesson_order.isdigit() or int(lesson_order) < 1:

            connection.close()

            return render_template(
                "admin_edit_lesson.html",
                lesson=lesson,
                topics=topics,
                error=(
                    "Lesson order deve essere "
                    "un numero positivo."
                )
            )

        topic_id = int(topic_id)
        lesson_order = int(lesson_order)

        # -----------------------------------------------------
        # CHECK TOPIC
        # -----------------------------------------------------

        cursor.execute("""
            SELECT id
            FROM topics
            WHERE id = ?
            AND course_id = ?
        """, (
            topic_id,
            course_id
        ))

        topic = cursor.fetchone()

        if topic is None:

            connection.close()

            return render_template(
                "admin_edit_lesson.html",
                lesson=lesson,
                topics=topics,
                error="Il topic selezionato non è valido."
            )

        # -----------------------------------------------------
        # CHECK LESSON ORDER
        # -----------------------------------------------------

        cursor.execute("""
            SELECT id
            FROM lessons
            WHERE topic_id = ?
            AND lesson_order = ?
            AND id != ?
        """, (
            topic_id,
            lesson_order,
            lesson_id
        ))

        existing_lesson = cursor.fetchone()

        if existing_lesson is not None:

            connection.close()

            return render_template(
                "admin_edit_lesson.html",
                lesson=lesson,
                topics=topics,
                error=(
                    "Esiste già un'altra lezione con "
                    "questo ordine nel topic selezionato."
                )
            )

        # -----------------------------------------------------
        # UPDATE
        # -----------------------------------------------------

        cursor.execute("""
            UPDATE lessons
            SET
                title = ?,
                topic_id = ?,
                lesson_order = ?
            WHERE id = ?
        """, (
            title,
            topic_id,
            lesson_order,
            lesson_id
        ))

        connection.commit()
        connection.close()

        return redirect("/admin/lessons")

    # ---------------------------------------------------------
    # SHOW EDIT PAGE
    # ---------------------------------------------------------

    connection.close()

    return render_template(
        "admin_edit_lesson.html",
        lesson=lesson,
        topics=topics
    )

@app.route(
    "/admin/lessons/<int:lesson_id>/delete",
    methods=["POST"]
)
@admin_required
def admin_delete_lesson(lesson_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    # ---------------------------------------------------------
    # CHECK LESSON
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT
            lessons.id
        FROM lessons
        JOIN topics
            ON lessons.topic_id = topics.id
        JOIN courses
            ON topics.course_id = courses.id
        WHERE lessons.id = ?
        AND courses.name = ?
    """, (
        lesson_id,
        "Python"
    ))

    lesson = cursor.fetchone()

    if lesson is None:
        connection.close()
        return "Lesson not found", 404

    # ---------------------------------------------------------
    # DELETE LESSON BLOCKS
    # ---------------------------------------------------------

    cursor.execute("""
        DELETE FROM lesson_blocks
        WHERE lesson_id = ?
    """, (lesson_id,))

    # ---------------------------------------------------------
    # DELETE LESSON
    # ---------------------------------------------------------

    cursor.execute("""
        DELETE FROM lessons
        WHERE id = ?
    """, (lesson_id,))

    connection.commit()
    connection.close()

    return redirect("/admin/lessons")

@app.route("/admin/lessons/<int:lesson_id>/blocks")
@admin_required
def admin_lesson_blocks(lesson_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    # Get lesson
    cursor.execute("""
        SELECT
            lessons.id,
            lessons.title,
            lessons.lesson_order,
            topics.name
        FROM lessons
        JOIN topics
            ON lessons.topic_id = topics.id
        WHERE lessons.id = ?
    """, (lesson_id,))

    lesson = cursor.fetchone()

    if lesson is None:
        connection.close()
        return "Lesson not found", 404

    # Get lesson blocks
    cursor.execute("""
        SELECT
            id,
            block_type,
            content,
            block_order
        FROM lesson_blocks
        WHERE lesson_id = ?
        ORDER BY block_order
    """, (lesson_id,))

    blocks = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_lesson_blocks.html",
        lesson=lesson,
        blocks=blocks
    )

@app.route(
    "/admin/lessons/<int:lesson_id>/blocks/add",
    methods=["GET", "POST"]
)
@admin_required
def admin_add_lesson_block(lesson_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    # ---------------------------------------------------------
    # CHECK LESSON
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT
            lessons.id,
            lessons.title
        FROM lessons
        JOIN topics
            ON lessons.topic_id = topics.id
        JOIN courses
            ON topics.course_id = courses.id
        WHERE lessons.id = ?
        AND courses.name = ?
    """, (
        lesson_id,
        "Python"
    ))

    lesson = cursor.fetchone()

    if lesson is None:
        connection.close()
        return "Lesson not found", 404

    # ---------------------------------------------------------
    # ADD BLOCK
    # ---------------------------------------------------------

    if request.method == "POST":

        block_type = request.form.get(
            "block_type",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        block_order = request.form.get(
            "block_order",
            ""
        ).strip()

        # -----------------------------------------------------
        # REQUIRED FIELDS
        # -----------------------------------------------------

        if not block_type or not content or not block_order:

            connection.close()

            return render_template(
                "admin_add_lesson_block.html",
                lesson=lesson,
                error="Tutti i campi sono obbligatori."
            )

        # -----------------------------------------------------
        # VALID BLOCK TYPES
        # -----------------------------------------------------

        valid_block_types = (
            "text",
            "explanation",
            "code",
            "output",
            "warning",
            "example",
            "exercise"
        )

        if block_type not in valid_block_types:

            connection.close()

            return render_template(
                "admin_add_lesson_block.html",
                lesson=lesson,
                error="Block type non valido."
            )

        # -----------------------------------------------------
        # VALID BLOCK ORDER
        # -----------------------------------------------------

        if not block_order.isdigit():

            connection.close()

            return render_template(
                "admin_add_lesson_block.html",
                lesson=lesson,
                error=(
                    "Block order deve essere "
                    "un numero positivo."
                )
            )

        block_order = int(block_order)

        if block_order < 1:

            connection.close()

            return render_template(
                "admin_add_lesson_block.html",
                lesson=lesson,
                error=(
                    "Block order deve essere "
                    "maggiore di zero."
                )
            )

        # -----------------------------------------------------
        # CHECK DUPLICATE ORDER
        # -----------------------------------------------------

        cursor.execute("""
            SELECT id
            FROM lesson_blocks
            WHERE lesson_id = ?
            AND block_order = ?
        """, (
            lesson_id,
            block_order
        ))

        existing_block = cursor.fetchone()

        if existing_block is not None:

            connection.close()

            return render_template(
                "admin_add_lesson_block.html",
                lesson=lesson,
                error=(
                    "Esiste già un blocco con questo "
                    "ordine nella lezione."
                )
            )

        # -----------------------------------------------------
        # INSERT BLOCK
        # -----------------------------------------------------

        cursor.execute("""
            INSERT INTO lesson_blocks (
                lesson_id,
                block_type,
                content,
                block_order
            )
            VALUES (?, ?, ?, ?)
        """, (
            lesson_id,
            block_type,
            content,
            block_order
        ))

        connection.commit()
        connection.close()

        return redirect(
            f"/admin/lessons/{lesson_id}/blocks"
        )

    # ---------------------------------------------------------
    # SHOW PAGE
    # ---------------------------------------------------------

    connection.close()

    return render_template(
        "admin_add_lesson_block.html",
        lesson=lesson
    )

@app.route(
    "/admin/lessons/<int:lesson_id>/blocks/edit/<int:block_id>",
    methods=["GET", "POST"]
)
@admin_required
def admin_edit_lesson_block(lesson_id, block_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    # ---------------------------------------------------------
    # CHECK LESSON
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT
            lessons.id,
            lessons.title
        FROM lessons
        JOIN topics
            ON lessons.topic_id = topics.id
        JOIN courses
            ON topics.course_id = courses.id
        WHERE lessons.id = ?
        AND courses.name = ?
    """, (
        lesson_id,
        "Python"
    ))

    lesson = cursor.fetchone()

    if lesson is None:
        connection.close()
        return "Lesson not found", 404

    # ---------------------------------------------------------
    # GET BLOCK
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT
            id,
            block_type,
            content,
            block_order
        FROM lesson_blocks
        WHERE id = ?
        AND lesson_id = ?
    """, (
        block_id,
        lesson_id
    ))

    block = cursor.fetchone()

    if block is None:
        connection.close()
        return "Block not found", 404

    # ---------------------------------------------------------
    # UPDATE BLOCK
    # ---------------------------------------------------------

    if request.method == "POST":

        block_type = request.form.get(
            "block_type",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        block_order = request.form.get(
            "block_order",
            ""
        ).strip()

        # -----------------------------------------------------
        # REQUIRED FIELDS
        # -----------------------------------------------------

        if not block_type or not content or not block_order:

            connection.close()

            return render_template(
                "admin_edit_lesson_block.html",
                lesson=lesson,
                block=block,
                error="Tutti i campi sono obbligatori."
            )

        # -----------------------------------------------------
        # VALID BLOCK TYPES
        # -----------------------------------------------------

        valid_block_types = (
            "text",
            "explanation",
            "code",
            "output",
            "warning",
            "example",
            "exercise"
        )

        if block_type not in valid_block_types:

            connection.close()

            return render_template(
                "admin_edit_lesson_block.html",
                lesson=lesson,
                block=block,
                error="Block type non valido."
            )

        # -----------------------------------------------------
        # VALID BLOCK ORDER
        # -----------------------------------------------------

        if not block_order.isdigit():

            connection.close()

            return render_template(
                "admin_edit_lesson_block.html",
                lesson=lesson,
                block=block,
                error=(
                    "Block order deve essere "
                    "un numero positivo."
                )
            )

        block_order = int(block_order)

        if block_order < 1:

            connection.close()

            return render_template(
                "admin_edit_lesson_block.html",
                lesson=lesson,
                block=block,
                error=(
                    "Block order deve essere "
                    "maggiore di zero."
                )
            )

        # -----------------------------------------------------
        # CHECK DUPLICATE ORDER
        # -----------------------------------------------------

        cursor.execute("""
            SELECT id
            FROM lesson_blocks
            WHERE lesson_id = ?
            AND block_order = ?
            AND id != ?
        """, (
            lesson_id,
            block_order,
            block_id
        ))

        existing_block = cursor.fetchone()

        if existing_block is not None:

            connection.close()

            return render_template(
                "admin_edit_lesson_block.html",
                lesson=lesson,
                block=block,
                error=(
                    "Esiste già un altro blocco con "
                    "questo ordine nella lezione."
                )
            )

        # -----------------------------------------------------
        # UPDATE BLOCK
        # -----------------------------------------------------

        cursor.execute("""
            UPDATE lesson_blocks
            SET
                block_type = ?,
                content = ?,
                block_order = ?
            WHERE id = ?
            AND lesson_id = ?
        """, (
            block_type,
            content,
            block_order,
            block_id,
            lesson_id
        ))

        connection.commit()
        connection.close()

        return redirect(
            f"/admin/lessons/{lesson_id}/blocks"
        )

    # ---------------------------------------------------------
    # SHOW EDIT PAGE
    # ---------------------------------------------------------

    connection.close()

    return render_template(
        "admin_edit_lesson_block.html",
        lesson=lesson,
        block=block
    )

@app.route(
    "/admin/lessons/<int:lesson_id>/blocks/delete/<int:block_id>",
    methods=["POST"]
)
@admin_required
def admin_delete_lesson_block(lesson_id, block_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM lesson_blocks
        WHERE id = ?
        AND lesson_id = ?
    """, (
        block_id,
        lesson_id
    ))

    block = cursor.fetchone()

    if block is None:
        connection.close()
        return "Block not found", 404

    cursor.execute("""
        DELETE FROM lesson_blocks
        WHERE id = ?
        AND lesson_id = ?
    """, (
        block_id,
        lesson_id
    ))

    connection.commit()
    connection.close()

    return redirect(
        f"/admin/lessons/{lesson_id}/blocks"
    )

if __name__ == "__main__":
    init_db()
    seed_data()
    app.run()
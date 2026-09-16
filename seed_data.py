import sqlite3
from data.lessons_basics import (
    INTRODUCTION_BLOCKS,
    PRINT_BLOCKS,
    VARIABLES_BLOCKS,
    DATA_TYPES_BLOCKS,
    INPUT_BLOCKS,
    TYPE_CONVERSION_BLOCKS
)

def seed_lesson_blocks(
    cursor,
    lesson_title,
    topic_id,
    blocks
):

    # ---------------------------------------------------------
    # GET LESSON
    # ---------------------------------------------------------

    cursor.execute("""
        SELECT id
        FROM lessons
        WHERE title = ?
        AND topic_id = ?
    """, (
        lesson_title,
        topic_id
    ))

    lesson = cursor.fetchone()

    if lesson is None:
        return

    lesson_id = lesson[0]

    # ---------------------------------------------------------
    # INSERT OR UPDATE BLOCKS
    # ---------------------------------------------------------

    for block_type, content, block_order in blocks:

        clean_content = content.strip()

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

        # -----------------------------------------------------
        # BLOCK DOES NOT EXIST → INSERT
        # -----------------------------------------------------

        if existing_block is None:

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
                clean_content,
                block_order
            ))

        # -----------------------------------------------------
        # BLOCK ALREADY EXISTS → UPDATE
        # -----------------------------------------------------

        else:

            block_id = existing_block[0]

            cursor.execute("""
                UPDATE lesson_blocks
                SET
                    block_type = ?,
                    content = ?
                WHERE id = ?
            """, (
                block_type,
                clean_content,
                block_id
            ))

            
def seed_data():

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    # =========================================================
    # 1. CREATE PYTHON COURSE
    # =========================================================

    cursor.execute("""
        INSERT OR IGNORE INTO courses (name)
        VALUES (?)
    """, ("Python",))

    cursor.execute("""
        SELECT id
        FROM courses
        WHERE name = ?
    """, ("Python",))

    python_course = cursor.fetchone()
    python_course_id = python_course[0]

    # =========================================================
    # 2. CREATE PYTHON TOPICS
    # =========================================================

    python_topics = [
        "Basics",
        "Data Types",
        "Control Flow",
        "Functions",
        "OOP",
        "Exceptions"
    ]

    for topic_name in python_topics:

        cursor.execute("""
            SELECT id
            FROM topics
            WHERE name = ?
            AND course_id = ?
        """, (
            topic_name,
            python_course_id
        ))

        existing_topic = cursor.fetchone()

        if existing_topic is None:

            cursor.execute("""
                INSERT INTO topics (
                    name,
                    course_id
                )
                VALUES (?, ?)
            """, (
                topic_name,
                python_course_id
            ))

    # =========================================================
    # 3. GET BASICS TOPIC
    # =========================================================

    cursor.execute("""
        SELECT id
        FROM topics
        WHERE name = ?
        AND course_id = ?
    """, (
        "Basics",
        python_course_id
    ))

    basics_topic = cursor.fetchone()

    basics_topic_id = basics_topic[0]

    # =========================================================
    # 4. CREATE BASICS LESSONS
    # =========================================================

    basics_lessons = [
        ("Introduction to Python", 1),
        ("print()", 2),
        ("Variables", 3),
        ("Data Types", 4),
        ("input()", 5),
        ("Type Conversion", 6)
    ]

    for title, lesson_order in basics_lessons:

        cursor.execute("""
            SELECT id
            FROM lessons
            WHERE title = ?
            AND topic_id = ?
        """, (
            title,
            basics_topic_id
        ))

        existing_lesson = cursor.fetchone()

        if existing_lesson is None:

            cursor.execute("""
                INSERT INTO lessons (
                    title,
                    topic_id,
                    lesson_order
                )
                VALUES (?, ?, ?)
            """, (
                title,
                basics_topic_id,
                lesson_order
            ))

    # =========================================================
    # 5. CREATE LESSON BLOCKS
    # =========================================================

    seed_lesson_blocks(
        cursor,
        "Introduction to Python",
        basics_topic_id,
        INTRODUCTION_BLOCKS
    )

    seed_lesson_blocks(
        cursor,
        "print()",
        basics_topic_id,
        PRINT_BLOCKS
    )

    seed_lesson_blocks(
        cursor,
        "Variables",
        basics_topic_id,
        VARIABLES_BLOCKS
    )

    seed_lesson_blocks(
        cursor,
        "Data Types",
        basics_topic_id,
        DATA_TYPES_BLOCKS
    )

    seed_lesson_blocks(
        cursor,
        "input()",
        basics_topic_id,
        INPUT_BLOCKS
    )

    seed_lesson_blocks(
        cursor,
        "Type Conversion",
        basics_topic_id,
        TYPE_CONVERSION_BLOCKS
    )


    # =========================================================
    # 6. CREATE INITIAL QUIZ QUESTIONS
    # =========================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM questions
    """)

    question_count = cursor.fetchone()[0]

    if question_count == 0:

        initial_questions = [

            (
                "Which Python library is commonly used for machine learning?",
                "Flask",
                "scikit-learn",
                "SQLite",
                "Bootstrap",
                "scikit-learn",
                basics_topic_id,
                "Beginner"
            ),

            (
                "Which keyword is used to define a function in Python?",
                "func",
                "define",
                "def",
                "function",
                "def",
                basics_topic_id,
                "Beginner"
            ),

            (
                "Which of these is a Python web framework?",
                "Flask",
                "NumPy",
                "Pandas",
                "Matplotlib",
                "Flask",
                basics_topic_id,
                "Beginner"
            )

        ]

        for question in initial_questions:

            cursor.execute("""
                INSERT INTO questions (
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
                question[0],
                question[1],
                question[2],
                question[3],
                question[4],
                question[5],
                python_course_id,
                question[6],
                question[7]
            ))

    # =========================================================
    # SAVE
    # =========================================================

    connection.commit()
    connection.close()
import sqlite3


def init_db():

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # =========================================================
    # ENABLE FOREIGN KEYS
    # =========================================================

    cursor.execute("PRAGMA foreign_keys = ON")

    # =========================================================
    # USERS
    # =========================================================

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

    # =========================================================
    # COURSES
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # =========================================================
    # TOPICS
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY (course_id)
                REFERENCES courses(id)
        )
    """)

    # =========================================================
    # LESSONS
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            topic_id INTEGER NOT NULL,
            lesson_order INTEGER NOT NULL,
            FOREIGN KEY (topic_id)
                REFERENCES topics(id)
        )
    """)

    # =========================================================
    # LESSON BLOCKS
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lesson_blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER NOT NULL,
            block_type TEXT NOT NULL,
            content TEXT NOT NULL,
            block_order INTEGER NOT NULL,
            FOREIGN KEY (lesson_id)
                REFERENCES lessons(id)
        )
    """)

    # =========================================================
    # QUESTIONS
    # =========================================================

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

            FOREIGN KEY (course_id)
                REFERENCES courses(id),

            FOREIGN KEY (topic_id)
                REFERENCES topics(id)
        )
    """)

    connection.commit()
    connection.close()
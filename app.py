from flask import Flask, render_template, request, redirect
import os
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


def init_db():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    book_id VARCHAR(50) UNIQUE,
                    title VARCHAR(255),
                    author VARCHAR(255),
                    status VARCHAR(20) DEFAULT 'Yes'
                );
            ''')
        conn.commit()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book_id = request.form["book_id"]
        title = request.form["title"]
        author = request.form["author"]

        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    '''
                    INSERT INTO books
                    (book_id, title, author, status)
                    VALUES (%s, %s, %s, %s)
                    ''',
                    (book_id, title, author, "Yes")
                )
            conn.commit()

        return redirect("/view")

    return render_template("add.html")


@app.route("/view")
def view_books():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT book_id, title, author, status
                FROM books
                ORDER BY id DESC
            ''')
            rows = cur.fetchall()

    books = [
        {
            "id": row["book_id"],
            "title": row["title"],
            "author": row["author"],
            "status": row["status"]
        }
        for row in rows
    ]

    return render_template("view.html", books=books)


@app.route("/search", methods=["GET", "POST"])
def search():
    results = []

    if request.method == "POST":
        keyword = request.form["keyword"]

        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    '''
                    SELECT book_id, title, author, status
                    FROM books
                    WHERE LOWER(title) LIKE LOWER(%s)
                       OR LOWER(author) LIKE LOWER(%s)
                    ''',
                    (f"%{keyword}%", f"%{keyword}%")
                )
                results = cur.fetchall()

    return render_template("search.html", results=results)


init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

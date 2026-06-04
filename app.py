from flask import Flask, render_template, request, redirect
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(**name**)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
return psycopg2.connect(
DATABASE_URL,
cursor_factory=RealDictCursor
)

def init_db():
conn = get_db()
cur = conn.cursor()

```
cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        book_id VARCHAR(50) UNIQUE,
        title VARCHAR(255),
        author VARCHAR(255),
        status VARCHAR(20) DEFAULT 'Yes'
    );
""")

conn.commit()
cur.close()
conn.close()
```

@app.route("/")
def home():
return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add_book():

```
if request.method == "POST":

    book_id = request.form["book_id"]
    title = request.form["title"]
    author = request.form["author"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO books
        (book_id,title,author,status)
        VALUES (%s,%s,%s,%s)
        """,
        (book_id, title, author, "Yes")
    )

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/view")

return render_template("add.html")
```

@app.route("/view")
def view_books():

```
conn = get_db()
cur = conn.cursor()

cur.execute("""
    SELECT book_id,title,author,status
    FROM books
    ORDER BY id DESC
""")

rows = cur.fetchall()

books = []

for row in rows:
    books.append({
        "id": row["book_id"],
        "title": row["title"],
        "author": row["author"],
        "status": row["status"]
    })

cur.close()
conn.close()

return render_template("view.html", books=books)
```

@app.route("/search", methods=["GET", "POST"])
def search():

```
results = []

if request.method == "POST":

    keyword = request.form["keyword"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT book_id,title,author,status
        FROM books
        WHERE
        LOWER(title) LIKE LOWER(%s)
        OR LOWER(author) LIKE LOWER(%s)
        """,
        (f"%{keyword}%", f"%{keyword}%")
    )

    rows = cur.fetchall()

    for row in rows:
        results.append({
            "id": row["book_id"],
            "title": row["title"],
            "author": row["author"],
            "status": row["status"]
        })

    cur.close()
    conn.close()

return render_template("search.html", results=results)
```

init_db()

if **name** == "**main**":
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

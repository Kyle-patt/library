from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
BOOK_FILE = "books.txt"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book_id = request.form["book_id"]
        title = request.form["title"]
        author = request.form["author"]
        with open(BOOK_FILE, "a") as f:
            f.write(f"{book_id},{title},{author},Yes\n")
        return redirect("/view")
    return render_template("add.html")

@app.route("/view")
def view_books():
    books = []
    try:
        with open(BOOK_FILE, "r") as f:
            for line in f:
                book_id, title, author, status = line.strip().split(",")
                books.append({"id": book_id, "title": title, "author": author, "status": status})
    except FileNotFoundError:
        pass
    return render_template("view.html", books=books)

@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        keyword = request.form["keyword"].lower()
        with open(BOOK_FILE, "r") as f:
            for line in f:
                book_id, title, author, status = line.strip().split(",")
                if keyword in title.lower() or keyword in author.lower():
                    results.append({"id": book_id, "title": title, "author": author, "status": status})
    return render_template("search.html", results=results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

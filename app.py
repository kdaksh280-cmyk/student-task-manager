from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "daksh_secret"

def connect_db():
    return sqlite3.connect("database.db")

# Create table
def create_table():
    db = connect_db()
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY,
            title TEXT,
            priority TEXT,
            date TEXT
        )
    """)
    db.commit()
    db.close()
create_table()

# LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "daksh" and password == "1234":
            session["user"] = username
            return redirect("/home")
        else:
            return "Wrong Login"

    return render_template("login.html")


# HOME PAGE
@app.route("/home")
def index():
    if "user" not in session:
        return redirect("/")

    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    db.close()

    return render_template("index.html", tasks=tasks)


# ADD TASK
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    priority = request.form["priority"]
    date = request.form["date"]

    db = connect_db()
    cur = db.cursor()
    cur.execute("INSERT INTO tasks(title, priority, date) VALUES(?,?,?)",
                (title, priority, date))
    db.commit()
    db.close()

    return redirect("/home")

@app.route("/delete/<id>")
def delete(id):
    db = connect_db()
    cur = db.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    db.commit()
    db.close()

    return redirect("/home")



# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

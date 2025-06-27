from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'users.db'

# ✅ Initialize SQLite DB if not exists
def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()
            print("Database initialized.")

# ✅ Home page route with form
@app.route('/')
def form():
    return render_template("registration.html")

# ✅ Handle form submission
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
        return f"<h3 style='text-align:center;'>Thanks for registering, {name}!</h3>"
    except Exception as e:
        return f"<h3 style='color:red; text-align:center;'>Error: {e}</h3>"

# ✅ Run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
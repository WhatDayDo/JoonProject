from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Home Page
@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add Task
@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    reminder_time = request.form['reminder_time']
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name, reminder_time) VALUES (?, ?)", (task_name, reminder_time))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

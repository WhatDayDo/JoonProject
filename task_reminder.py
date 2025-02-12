from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# 📌 Home Route - Redirect to Login or Task Page
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('task_page'))  # Redirect to Task Page

# 📌 User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect(url_for('login'))  
        except sqlite3.IntegrityError:
            return "Username already exists. Choose another."

        conn.close()
    
    return render_template('register.html')

# 📌 User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username  
            return redirect(url_for('task_page'))  
        else:
            return "Invalid username or password."

    return render_template('login.html')

# 📌 User Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# 📌 Task Page
@app.route('/tasks')
def task_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE datetime(reminder_time) >= datetime('now','+7 hours') AND user_id = ?", (session['user_id'],))
    tasks = cursor.fetchall()
    conn.close()

    return render_template('tasks.html', tasks=tasks, username=session.get('username'))

# 📌 Work Page
@app.route('/works')
def work_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, name FROM Works WHERE status = 1 AND user_id = ?", (session['user_id'],))
    works = cursor.fetchall()
    conn.close()

    return render_template('works.html', works=works, username=session.get('username'))

# 📌 Add Task
@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    task_name = request.form['task_name']
    reminder_time = request.form['reminder_time']

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name, reminder_time, user_id) VALUES (?, ?, ?)", 
                   (task_name, reminder_time, session['user_id']))
    conn.commit()
    conn.close()

    return redirect(url_for('task_page'))

# 📌 Add Work
@app.route('/add_work', methods=['POST'])
def add_work():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    work_name = request.form['work_name']

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Works (name, user_id) VALUES (?, ?)", 
                   (work_name, session['user_id']))
    conn.commit()
    conn.close()

    return redirect(url_for('work_page'))

#Route to Soft Delete a Work Task
@app.route('/delete_work/<int:work_id>', methods=['POST'])
def delete_work(work_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Works SET status = 0 WHERE rowid = ?", (work_id,))
    conn.commit()
    conn.close()
    return {"success": True} 

#Route to Fetch Active Work Tasks    
@app.route('/get_work_tasks')
def get_work_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, name FROM Works WHERE status = 1 AND user_id = ?", (session['user_id'],))
    work_tasks = cursor.fetchall()
    conn.close()
    
    return {"tasks": work_tasks}

# 📌 Run Flask App
if __name__ == "__main__":
    app.run(debug=True)

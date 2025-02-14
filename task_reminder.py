from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, Response  # Import jsonify
import sqlite3
import base64

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
    cursor.execute("SELECT rowid, name, image FROM Works WHERE user_id = ? AND status = 1", (session['user_id'],))
    works = cursor.fetchall()
    conn.close()

    # Convert BLOB to Base64 for HTML display
    works_with_images = [
         (row[0], row[1], base64.b64encode(row[2]).decode('utf-8') if row[2] else None) 
         for row in works
     ]

    return render_template('works.html', works=works_with_images, username=session.get('username'))


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

from flask import jsonify  # Import jsonify

@app.route('/get_tasks')
def get_tasks():
    if 'user_id' not in session:
        return jsonify([])  # Return empty list if not logged in

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, reminder_time FROM tasks WHERE user_id = ?", (session['user_id'],))
    tasks = cursor.fetchall()
    conn.close()

    # Convert tasks to JSON-friendly format
    tasks_data = [{"id": t[0], "name": t[1], "reminder_time": t[2]} for t in tasks]

    return jsonify(tasks_data)


# 📌 Add Work
@app.route('/add_work', methods=['POST'])
def add_work():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    work_name = request.form['work_name']
    image = request.files.get('image')  # Get uploaded image

    image_data = None
    if image and image.filename != '':
        image_data = image.read()  # Read image as binary data

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Works (name, image, user_id) 
        VALUES (?, ?, ?)
    """, (work_name, image_data, session['user_id']))
    conn.commit()
    conn.close()

    return redirect(url_for('work_page'))


@app.route('/view_work_image')
def view_work_image():
    if 'user_id' not in session:
        return "User not logged in", 401

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    # Fetch the first image associated with the current user
    cursor.execute("SELECT image FROM Works WHERE user_id = ? LIMIT 1", (session['user_id'],))
    image_data = cursor.fetchone()
    conn.close()

    if image_data and image_data[0]:
        # Send the image in the response
        return Response(image_data[0], mimetype='image/png')
    return "No image available", 404


#Route to Soft Delete a Work Task 
@app.route('/delete_work/<int:work_id>', methods=['POST'])
def delete_work(work_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Works SET status = 0 WHERE rowid = ?", (work_id,))
    conn.commit()
    conn.close()
    
    return {"success": True}



# 📌 Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Home Page
@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    # Fetch tasks
    cursor.execute("SELECT * FROM tasks WHERE datetime(reminder_time) >= datetime('now','+7 hours')")
    tasks = cursor.fetchall()
    
    # Fetch works
    cursor.execute("SELECT id, name FROM Works where status = 1")
    works = cursor.fetchall()
    
    conn.close()
    return render_template('index.html', tasks=tasks, works=works)

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

# Save Work
@app.route('/save_work', methods=['POST'])
def save_work():
    work_name = request.form['work_name']
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Works (Name) VALUES (?)", (work_name,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

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
    cursor.execute("SELECT rowid, name FROM Works WHERE status = 1")
    work_tasks = cursor.fetchall()
    conn.close()
    
    return {"tasks": work_tasks}



# Run the app
if __name__ == "__main__":
    app.run(debug=True)

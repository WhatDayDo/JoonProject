import sqlite3

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Add a user_id column to tasks table to associate tasks with users
cursor.execute("""
ALTER TABLE tasks ADD COLUMN user_id INTEGER DEFAULT NULL
""")

# Add a user_id column to works table
cursor.execute("""
ALTER TABLE Works ADD COLUMN user_id INTEGER DEFAULT NULL
""")

conn.commit()
conn.close()

print("Database updated with user authentication support!")


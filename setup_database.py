import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create the tasks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    reminder_time TEXT NOT NULL
)
""")
conn.close()
print("Database setup complete!")

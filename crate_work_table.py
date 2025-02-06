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
cursor.execute("""
CREATE TABLE IF NOT EXISTS Works (
    "Name" TEXT NOT NULL,
 "ID" INTEGER PRIMARY KEY AUTOINCREMENT
)
""")
conn.close()
print("Database setup complete!")
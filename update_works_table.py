import sqlite3

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Add the "status" column if it doesn't already exist
cursor.execute("ALTER TABLE Works ADD COLUMN status INTEGER DEFAULT 1")

conn.commit()
conn.close()
print("Database updated with 'status' column!")

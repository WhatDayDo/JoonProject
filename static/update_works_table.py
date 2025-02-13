import sqlite3

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Add the "image" column if it doesn't exist
cursor.execute("""
    ALTER TABLE Works ADD COLUMN image BLOB
""")

conn.commit()
conn.close()

print("Database updated with 'image' column in Works table!")

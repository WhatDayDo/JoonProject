import sqlite3

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Add an "image_path" column instead of BLOB storage
cursor.execute("""
    ALTER TABLE Works ADD COLUMN image_path TEXT
""")

conn.commit()
conn.close()

print("Database updated to store image paths instead of binary data!")

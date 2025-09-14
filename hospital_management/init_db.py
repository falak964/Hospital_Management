import sqlite3

# Connect database
conn = sqlite3.connect("hospital.db")
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')

#sample user
c.execute("INSERT OR IGNORE INTO user (username, password) VALUES (?, ?)", ("admin", "admin123"))

conn.commit()
conn.close()

print("Database and 'user' table created successfully.")


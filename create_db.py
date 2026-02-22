import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect("student_grades.db")
cursor = connection.cursor()

# Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY,
        name TEXT,
        subject TEXT,
        score INTEGER,
        grade TEXT
    )
""")


# Insert some dummy data
data = [
    (1, "Aman", "Math", 95, "A"),
    (2, "Anshu", "Math", 78, "C"),
    (3, "Akshu", "Math", 88, "B"),
    (4, "Rahul", "Math", 92, "A"),
    (5, "Divyansh", "Math", 85, "B"),
    (6, "Nandini", "Math", 65, "D"),
    (7, "Aman", "Science", 95, "A"),
    (8, "Anshu", "Science", 78, "C"),
    (9, "Akshu", "Science", 88, "B"),
    (10, "Rahul", "Science", 92, "A"),
    (11, "Divyansh", "Science", 85, "B"),
    (12, "Nandini", "Science", 65, "D"),
    (13, "Aman", "History", 95, "A"),
    (14, "Anshu", "History", 78, "C"),
    (15, "Akshu", "History", 88, "B"),
    (16, "Rahul", "History", 92, "A"),
    (17, "Divyansh", "History", 85, "B"),
    (18, "Nandini", "History", 65, "D")
]

cursor.executemany("INSERT OR IGNORE INTO grades VALUES (?, ?, ?, ?, ?)", data)
connection.commit()
connection.close()

print("Database created and populated successfully!")

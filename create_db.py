import sqlite3
import random

def get_grade(score):
    if score >= 90: return 'A'
    if score >= 80: return 'B'
    if score >= 70: return 'C'
    if score >= 60: return 'D'
    return 'F'

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

# Base names and subjects
names = [
    "Aman", "Anshu", "Akshu", "Rahul", "Divyansh", "Nandini",
    "Ishita", "Kabir", "Meera", "Rohan", "Sanya", "Vikram",
    "Zoya", "Arjun", "Priya", "Sahil"
]
subjects = ["Math", "Science", "History", "English", "Geography", "Physics"]

# Generate randomized data
data = []
id_counter = 1
for subject in subjects:
    for name in names:
        score = random.randint(50, 100)
        grade = get_grade(score)
        data.append((id_counter, name, subject, score, grade))
        id_counter += 1

# Use REPLACE to update existing rows with new random scores
cursor.executemany("INSERT OR REPLACE INTO grades VALUES (?, ?, ?, ?, ?)", data)
connection.commit()
connection.close()

print("Database created and populated with randomized scores!")

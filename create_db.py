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

# Drop existing tables to recreate with new schema
cursor.execute("DROP TABLE IF EXISTS grades")
cursor.execute("DROP TABLE IF EXISTS subjects")

# Create subjects table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        subject_name TEXT UNIQUE
    )
""")

# Create grades table (normalized)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY,
        student_name TEXT,
        subject_id INTEGER,
        score INTEGER,
        grade TEXT,
        FOREIGN KEY (subject_id) REFERENCES subjects (id)
    )
""")

# Base names and subjects
names = [
    "Aman", "Anshu", "Akshu", "Rahul", "Divyansh", "Nandini",
    "Ishita", "Kabir", "Meera", "Rohan", "Sanya", "Vikram",
    "Zoya", "Arjun", "Priya", "Sahil"
]
subject_list = ["Math", "Science", "History", "English", "Geography", "Physics"]

# Insert subjects and keep track of their IDs
subject_data = [(i+1, name) for i, name in enumerate(subject_list)]
cursor.executemany("INSERT INTO subjects VALUES (?, ?)", subject_data)

# Generate randomized data for grades
data = []
id_counter = 1
for subject_id, _ in subject_data:
    for name in names:
        score = random.randint(50, 100)
        grade = get_grade(score)
        data.append((id_counter, name, subject_id, score, grade))
        id_counter += 1

# Insert randomized grades
cursor.executemany("INSERT INTO grades VALUES (?, ?, ?, ?, ?)", data)
connection.commit()
connection.close()

print("Database created and populated with normalized tables!")

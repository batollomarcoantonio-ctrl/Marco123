from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Sample student data
students = [
    {"id": 1, "name": "Alice Santos", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Mark Dela Cruz", "grade": 11, "section": "Reuben"}
]

# Home route
@app.route('/')
def home():
    return "Welcome to the Student Management System API!"

# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# Get a single student by ID
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

# Add a new student via JSON (API)
@app.route('/student', methods=['POST'])
def add_student():
    new_student = request.get_json()
    if not new_student or "name" not in new_student or "grade" not in new_student or "section" not in new_student:
        return jsonify({"error": "Invalid data, please include name, grade, and section"}), 400

    new_student["id"] = len(students) + 1
    students.append(new_student)
    return jsonify({"message": "Student added successfully!", "student": new_student}), 201

# Add a new student via HTML form
@app.route('/add_student_form', methods=['GET', 'POST'])
def add_student_form():
    html_form = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Student</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f2f2f2; text-align: center; padding: 40px; }
            form { background: white; display: inline-block; padding: 20px 40px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            input { margin: 10px; padding: 10px; width: 80%; }
            button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #45a049; }
        </style>
    </head>
    <body>
        <h1>Add New Student</h1>
        <form method="POST">
            <input type="text" name="name" placeholder="Student Name" required><br>
            <input type="number" name="grade" placeholder="Grade Level" required><br>
            <input type="text" name="section" placeholder="Section" required><br>
            <button type="submit">Add Student</button>
        </form>
    </body>
    </html>
    '''
    if request.method == 'POST':
        name = request.form['name']
        grade = request.form['grade']
        section = request.form['section']
        new_student = {
            "id": len(students) + 1,
            "name": name,
            "grade": int(grade),
            "section": section
        }
        students.append(new_student)
        return f"<h2>✅ Student '{name}' added successfully!</h2><a href='/add_student_form'>Back</a>"

    return render_template_string(html_form)

if __name__ == '__main__':
    app.run(debug=True)

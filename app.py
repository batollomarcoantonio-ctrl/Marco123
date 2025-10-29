from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# In-memory student data
students = [
    {"id": 1, "name": "Alice Santos", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Mark Dela Cruz", "grade": 11, "section": "Reuben"}
]

# Home route with navigation
@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Management System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #f0f9ff, #cbebff);
                text-align: center;
                padding: 60px;
            }
            h1 {
                color: #333;
            }
            .btn {
                display: inline-block;
                margin: 10px;
                padding: 15px 30px;
                background-color: #007BFF;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                transition: 0.3s;
            }
            .btn:hover {
                background-color: #0056b3;
            }
            .container {
                background: white;
                display: inline-block;
                padding: 40px 60px;
                border-radius: 20px;
                box-shadow: 0 0 15px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Welcome to the Student Management System API</h1>
            <a href="/students" class="btn">📋 View All Students</a>
            <a href="/add_student_form" class="btn">➕ Add New Student</a>
            <a href="/search_student" class="btn">🔍 Search Student by ID</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    html = "<h1>📋 Student List</h1><ul>"
    for s in students:
        html += f"<li><b>ID:</b> {s['id']} | <b>Name:</b> {s['name']} | <b>Grade:</b> {s['grade']} | <b>Section:</b> {s['section']}</li>"
    html += "</ul><a href='/'>⬅ Back to Home</a>"
    return html

# Get a single student by ID
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return render_template_string(f"""
            <h1>🎯 Student Details</h1>
            <p><b>ID:</b> {student['id']}</p>
            <p><b>Name:</b> {student['name']}</p>
            <p><b>Grade:</b> {student['grade']}</p>
            <p><b>Section:</b> {student['section']}</p>
            <a href='/'>⬅ Back to Home</a>
        """)
    else:
        return render_template_string("""
            <h2>❌ Student Not Found</h2>
            <a href='/'>⬅ Back to Home</a>
        """)

# Search student by ID (via form)
@app.route('/search_student', methods=['GET', 'POST'])
def search_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        return f"<meta http-equiv='refresh' content='0; url=/student/{student_id}' />"
    html = '''
    <h1>🔍 Search Student by ID</h1>
    <form method="POST">
        <input type="number" name="student_id" placeholder="Enter Student ID" required>
        <button type="submit">Search</button>
    </form>
    <br><a href="/">⬅ Back to Home</a>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 100px; }
        input, button { padding: 10px; margin: 5px; }
        button { background: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
    '''
    return render_template_string(html)

# Add a new student via JSON (API)
@app.route('/student', methods=['POST'])
def add_student():
    new_student = request.get_json()
    if not new_student or "name" not in new_student or "grade" not in new_student or "section" not in new_student:
        return jsonify({"error": "Invalid data"}), 400

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
            body { font-family: Arial, sans-serif; background: #f0f9ff; text-align: center; padding: 40px; }
            form { background: white; display: inline-block; padding: 20px 40px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            input { margin: 10px; padding: 10px; width: 80%; }
            button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #45a049; }
        </style>
    </head>
    <body>
        <h1>➕ Add New Student</h1>
        <form method="POST">
            <input type="text" name="name" placeholder="Student Name" required><br>
            <input type="number" name="grade" placeholder="Grade Level" required><br>
            <input type="text" name="section" placeholder="Section" required><br>
            <button type="submit">Add Student</button>
        </form>
        <br><a href="/">⬅ Back to Home</a>
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
        return f"<h2>✅ Student '{name}' added successfully!</h2><a href='/'>⬅ Back to Home</a>"
    return render_template_string(html_form)

if __name__ == '__main__':
    app.run(debug=True)

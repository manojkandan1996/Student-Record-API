from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
api = Api(app)

students = []
student_id_counter = 1
valid_grades = {'A', 'B', 'C', 'D'}

class StudentListResource(Resource):
    def get(self):
        return {'students': students}, 200

    def post(self):
        global student_id_counter
        data = request.get_json()
        if not data or 'name' not in data or 'roll' not in data or 'grade' not in data:
            raise BadRequest("Name, roll, and grade are required.")

        if data['grade'] not in valid_grades:
            raise BadRequest("Grade must be one of A, B, C, or D.")

        new_student = {
            'id': student_id_counter,
            'name': data['name'],
            'roll': data['roll'],
            'grade': data['grade']
        }
        students.append(new_student)
        student_id_counter += 1
        return {'message': 'Student created successfully', 'student': new_student}, 201

class StudentResource(Resource):
    def get(self, id):
        student = next((s for s in students if s['id'] == id), None)
        if not student:
            raise NotFound("Student not found.")
        return student, 200

    def put(self, id):
        data = request.get_json()
        student = next((s for s in students if s['id'] == id), None)
        if not student:
            raise NotFound("Student not found.")

        if 'grade' in data and data['grade'] not in valid_grades:
            raise BadRequest("Grade must be one of A, B, C, or D.")

        if 'name' in data:
            student['name'] = data['name']
        if 'roll' in data:
            student['roll'] = data['roll']
        if 'grade' in data:
            student['grade'] = data['grade']

        return {'message': 'Student updated successfully', 'student': student}, 200

    def delete(self, id):
        global students
        student = next((s for s in students if s['id'] == id), None)
        if not student:
            raise NotFound("Student not found.")
        students = [s for s in students if s['id'] != id]
        return {'message': f'Student with id {id} deleted successfully.'}, 200

# Routes
api.add_resource(StudentListResource, '/students')
api.add_resource(StudentResource, '/students/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)

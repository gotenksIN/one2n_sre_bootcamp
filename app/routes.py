from flask import jsonify, request

from .extensions import db
from .models import Student


def init_routes(app):
    @app.route('/api/v1/healthcheck', methods=['GET'])
    def healthcheck():
        """Get API health status."""
        app.logger.debug("Healthcheck requested")
        return jsonify({"status": "healthy"}), 200

    @app.route('/api/v1/students', methods=['POST'])
    def add_student():
        """Create a new student."""
        data = request.get_json(silent=True)
        if not data or "name" not in data or "age" not in data:
            app.logger.warning("Student creation failed: missing name or age")
            return jsonify({"error": "Name and age are required"}), 400
        student = Student(name=data["name"], age=data["age"])
        db.session.add(student)
        db.session.commit()
        app.logger.info("Student created", extra={"student_id": student.id})
        return jsonify(student.to_dict()), 201

    @app.route('/api/v1/students', methods=['GET'])
    def get_students():
        """Retrieve all students."""
        students = Student.query.all()
        app.logger.debug("Students listed", extra={"student_count": len(students)})
        return jsonify([student.to_dict() for student in students]), 200

    @app.route('/api/v1/students/<int:student_id>', methods=['GET'])
    def get_student(student_id):
        """Retrieve a specific student by ID."""
        student = db.session.get(Student, student_id)
        if not student:
            app.logger.warning(
                "Student lookup failed", extra={"student_id": student_id}
            )
            return jsonify({"error": "Student not found"}), 404
        app.logger.debug("Student retrieved", extra={"student_id": student.id})
        return jsonify(student.to_dict()), 200

    @app.route('/api/v1/students/<int:student_id>', methods=['PUT'])
    def update_student(student_id):
        """Update a student record."""
        student = db.session.get(Student, student_id)
        if not student:
            app.logger.warning(
                "Student update failed: not found", extra={"student_id": student_id}
            )
            return jsonify({"error": "Student not found"}), 404
        data = request.get_json(silent=True)
        if not data:
            app.logger.warning(
                "Student update failed: invalid JSON payload",
                extra={"student_id": student_id},
            )
            return jsonify({"error": "Invalid JSON payload"}), 400
        if "name" in data:
            student.name = data["name"]
        if "age" in data:
            student.age = data["age"]
        db.session.commit()
        app.logger.info("Student updated", extra={"student_id": student.id})
        return jsonify(student.to_dict()), 200

    @app.route('/api/v1/students/<int:student_id>', methods=['DELETE'])
    def delete_student(student_id):
        """Delete a student record."""
        student = db.session.get(Student, student_id)
        if not student:
            app.logger.warning(
                "Student deletion failed: not found", extra={"student_id": student_id}
            )
            return jsonify({"error": "Student not found"}), 404
        db.session.delete(student)
        db.session.commit()
        app.logger.info("Student deleted", extra={"student_id": student_id})
        return jsonify({"message": "Student deleted successfully"}), 200

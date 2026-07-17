from flask import jsonify, request

from ...services import student_service
from . import api_v1


@api_v1.route('/students', methods=['POST'])
def add_student():
    """Create a new student."""
    data = request.get_json(silent=True)
    student = student_service.create_student(data)
    return jsonify(student.to_dict()), 201


@api_v1.route('/students', methods=['GET'])
def get_students():
    """Retrieve all students."""
    students = student_service.list_students()
    return jsonify([s.to_dict() for s in students]), 200


@api_v1.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Retrieve a specific student by ID."""
    student = student_service.get_student(student_id)
    return jsonify(student.to_dict()), 200


@api_v1.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update a student record."""
    data = request.get_json(silent=True)
    student = student_service.update_student(student_id, data)
    return jsonify(student.to_dict()), 200


@api_v1.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student record."""
    student_service.delete_student(student_id)
    return jsonify({"message": "Student deleted successfully"}), 200

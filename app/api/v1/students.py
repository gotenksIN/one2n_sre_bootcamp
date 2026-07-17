from flask import current_app, jsonify, request

from ...repositories.student_repository import (
    create,
    delete,
    get_by_id,
    list_all,
    update,
)
from ...schemas.student import validate_create_student, validate_update_student
from . import api_v1


@api_v1.route('/students', methods=['POST'])
def add_student():
    """Create a new student."""
    data = request.get_json(silent=True)
    validated = validate_create_student(data)
    student = create(validated["name"], validated["age"])
    current_app.logger.info("Student created", extra={"student_id": student.id})
    return jsonify(student.to_dict()), 201


@api_v1.route('/students', methods=['GET'])
def get_students():
    """Retrieve all students."""
    students = list_all()
    current_app.logger.debug(
        "Students listed", extra={"student_count": len(students)}
    )
    return jsonify([student.to_dict() for student in students]), 200


@api_v1.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Retrieve a specific student by ID."""
    student = get_by_id(student_id)
    if not student:
        current_app.logger.warning(
            "Student lookup failed", extra={"student_id": student_id}
        )
        return jsonify({"error": "Student not found"}), 404
    current_app.logger.debug("Student retrieved", extra={"student_id": student.id})
    return jsonify(student.to_dict()), 200


@api_v1.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update a student record."""
    student = get_by_id(student_id)
    if not student:
        current_app.logger.warning(
            "Student update failed: not found", extra={"student_id": student_id}
        )
        return jsonify({"error": "Student not found"}), 404
    data = request.get_json(silent=True)
    validated = validate_update_student(data)
    update(student, validated)
    current_app.logger.info("Student updated", extra={"student_id": student.id})
    return jsonify(student.to_dict()), 200


@api_v1.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student record."""
    student = get_by_id(student_id)
    if not student:
        current_app.logger.warning(
            "Student deletion failed: not found", extra={"student_id": student_id}
        )
        return jsonify({"error": "Student not found"}), 404
    delete(student)
    current_app.logger.info("Student deleted", extra={"student_id": student_id})
    return jsonify({"message": "Student deleted successfully"}), 200

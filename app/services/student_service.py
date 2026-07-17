from app.errors import NotFoundError
from app.repositories import student_repository as repo
from app.schemas.student import validate_create_student, validate_update_student


def create_student(data):
    validated = validate_create_student(data)
    return repo.create(validated["name"], validated["age"])


DEFAULT_LIMIT = 20
MAX_LIMIT = 100


def list_students(limit=DEFAULT_LIMIT, offset=0):
    students, total = repo.list_paginated(limit, offset)
    return {
        "students": students,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def get_student(student_id):
    student = repo.get_by_id(student_id)
    if student is None:
        raise NotFoundError("Student not found")
    return student


def update_student(student_id, data):
    student = get_student(student_id)
    validated = validate_update_student(data)
    return repo.update(student, validated)


def delete_student(student_id):
    student = get_student(student_id)
    repo.delete(student)

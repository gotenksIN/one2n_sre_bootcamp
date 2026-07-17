from app.extensions import db
from app.models import Student


def create(name, age):
    student = Student(name=name, age=age)
    db.session.add(student)
    db.session.commit()
    return student


def list_all():
    return Student.query.all()


def list_paginated(limit, offset):
    total = Student.query.count()
    students = (
        Student.query.order_by(Student.id).limit(limit).offset(offset).all()
    )
    return students, total


def get_by_id(student_id):
    return db.session.get(Student, student_id)


def update(student, data):
    if "name" in data:
        student.name = data["name"]
    if "age" in data:
        student.age = data["age"]
    db.session.commit()
    return student


def delete(student):
    db.session.delete(student)
    db.session.commit()

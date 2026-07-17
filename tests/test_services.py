from unittest.mock import MagicMock, patch

import pytest

from app.errors import NotFoundError, ValidationError
from app.services.student_service import (
    create_student,
    delete_student,
    get_student,
    list_students,
    update_student,
)


@pytest.fixture()
def mock_repo():
    with patch("app.services.student_service.repo") as mock:
        yield mock


class TestCreateStudent:
    def test_creates_student_via_repo(self, mock_repo):
        student = MagicMock()
        mock_repo.create.return_value = student

        result = create_student({"name": "Alice", "age": 21})

        mock_repo.create.assert_called_once_with("Alice", 21)
        assert result is student

    def test_invalid_data_raises_validation_error(self, mock_repo):
        with pytest.raises(ValidationError, match="Name and age are required"):
            create_student({"name": "Alice"})

        mock_repo.create.assert_not_called()


class TestListStudents:
    def test_returns_paginated_students_from_repo(self, mock_repo):
        students = [MagicMock(), MagicMock()]
        mock_repo.list_paginated.return_value = (students, 12)

        result = list_students(limit=5, offset=10)

        mock_repo.list_paginated.assert_called_once_with(5, 10)
        assert result == {
            "students": students,
            "total": 12,
            "limit": 5,
            "offset": 10,
        }

    def test_uses_default_limit_and_offset(self, mock_repo):
        students = []
        mock_repo.list_paginated.return_value = (students, 0)

        result = list_students()

        mock_repo.list_paginated.assert_called_once_with(20, 0)
        assert result["total"] == 0
        assert result["limit"] == 20


class TestGetStudent:
    def test_returns_student_when_found(self, mock_repo):
        student = MagicMock()
        mock_repo.get_by_id.return_value = student

        result = get_student(1)

        mock_repo.get_by_id.assert_called_once_with(1)
        assert result is student

    def test_raises_not_found_when_missing(self, mock_repo):
        mock_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Student not found"):
            get_student(999)


class TestUpdateStudent:
    def test_updates_existing_student(self, mock_repo):
        student = MagicMock()
        updated = MagicMock()
        mock_repo.get_by_id.return_value = student
        mock_repo.update.return_value = updated

        result = update_student(1, {"name": "Bob"})

        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.update.assert_called_once_with(student, {"name": "Bob"})
        assert result is updated

    def test_raises_not_found_when_missing(self, mock_repo):
        mock_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Student not found"):
            update_student(999, {"name": "Bob"})

        mock_repo.update.assert_not_called()

    def test_invalid_data_raises_validation_error(self, mock_repo):
        student = MagicMock()
        mock_repo.get_by_id.return_value = student

        with pytest.raises(ValidationError, match="Invalid JSON payload"):
            update_student(1, {})

        mock_repo.update.assert_not_called()


class TestDeleteStudent:
    def test_deletes_existing_student(self, mock_repo):
        student = MagicMock()
        mock_repo.get_by_id.return_value = student

        delete_student(1)

        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.delete.assert_called_once_with(student)

    def test_raises_not_found_when_missing(self, mock_repo):
        mock_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Student not found"):
            delete_student(999)

        mock_repo.delete.assert_not_called()

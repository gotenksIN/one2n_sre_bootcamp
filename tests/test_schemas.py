import pytest

from app.errors import ValidationError
from app.schemas.student import validate_create_student, validate_update_student


class TestValidateCreateStudent:
    def test_valid_data_returns_validated_dict(self):
        result = validate_create_student({"name": "Alice", "age": 21})

        assert result == {"name": "Alice", "age": 21}

    def test_missing_name_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Name and age are required"):
            validate_create_student({"age": 21})

    def test_missing_age_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Name and age are required"):
            validate_create_student({"name": "Alice"})

    def test_non_dict_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Request must be valid JSON"):
            validate_create_student(None)

    def test_non_string_name_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Name must be a non-empty string"):
            validate_create_student({"name": 123, "age": 21})

    def test_empty_name_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Name must be a non-empty string"):
            validate_create_student({"name": "  ", "age": 21})

    def test_non_integer_age_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Age must be an integer"):
            validate_create_student({"name": "Alice", "age": "21"})

    def test_boolean_age_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Age must be an integer"):
            validate_create_student({"name": "Alice", "age": True})


class TestValidateUpdateStudent:
    def test_valid_name_returns_validated_dict(self):
        result = validate_update_student({"name": "Bob"})

        assert result == {"name": "Bob"}

    def test_valid_age_returns_validated_dict(self):
        result = validate_update_student({"age": 30})

        assert result == {"age": 30}

    def test_valid_name_and_age_returns_validated_dict(self):
        result = validate_update_student({"name": "Bob", "age": 30})

        assert result == {"name": "Bob", "age": 30}

    def test_empty_dict_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Invalid JSON payload"):
            validate_update_student({})

    def test_non_dict_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Invalid JSON payload"):
            validate_update_student(None)

    def test_non_string_name_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Name must be a non-empty string"):
            validate_update_student({"name": 456})

    def test_empty_name_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Name must be a non-empty string"):
            validate_update_student({"name": ""})

    def test_non_integer_age_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Age must be an integer"):
            validate_update_student({"age": "young"})

    def test_boolean_age_raises_validation_error(self):
        with pytest.raises(ValidationError, match="Age must be an integer"):
            validate_update_student({"age": False})

from app.errors import ValidationError

MIN_AGE = 1
MAX_AGE = 150


def _validate_name(name):
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Name must be a non-empty string")
    return name.strip()


def _validate_age(age):
    if not isinstance(age, int) or isinstance(age, bool):
        raise ValidationError("Age must be an integer")
    if not (MIN_AGE <= age <= MAX_AGE):
        raise ValidationError(
            f"Age must be between {MIN_AGE} and {MAX_AGE}"
        )
    return age


def validate_create_student(data):
    if not isinstance(data, dict):
        raise ValidationError("Request must be valid JSON")
    if "name" not in data or "age" not in data:
        raise ValidationError("Name and age are required")
    return {
        "name": _validate_name(data["name"]),
        "age": _validate_age(data["age"]),
    }


def validate_update_student(data):
    if not isinstance(data, dict) or not data:
        raise ValidationError("Invalid JSON payload")
    validated = {}
    if "name" in data:
        validated["name"] = _validate_name(data["name"])
    if "age" in data:
        validated["age"] = _validate_age(data["age"])
    return validated

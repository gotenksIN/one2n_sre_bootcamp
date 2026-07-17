from app.errors import ValidationError


def validate_create_student(data):
    if not isinstance(data, dict):
        raise ValidationError("Request must be valid JSON")
    if "name" not in data or "age" not in data:
        raise ValidationError("Name and age are required")
    name = data.get("name")
    age = data.get("age")
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Name must be a non-empty string")
    if not isinstance(age, int) or isinstance(age, bool):
        raise ValidationError("Age must be an integer")
    return {"name": name, "age": age}


def validate_update_student(data):
    if not isinstance(data, dict) or not data:
        raise ValidationError("Invalid JSON payload")
    validated = {}
    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("Name must be a non-empty string")
        validated["name"] = name
    if "age" in data:
        age = data["age"]
        if not isinstance(age, int) or isinstance(age, bool):
            raise ValidationError("Age must be an integer")
        validated["age"] = age
    return validated

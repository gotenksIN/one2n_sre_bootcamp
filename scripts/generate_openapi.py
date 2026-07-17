import argparse
import json
from pathlib import Path

from apispec import APISpec


def _ref(name):
    return {"$ref": f"#/components/schemas/{name}"}


def _json(schema):
    return {"content": {"application/json": {"schema": schema}}}


def build_spec(version):
    spec = APISpec(
        title="Student REST API",
        version=version,
        openapi_version="3.0.2",
        info={"description": "CRUD REST API for managing student records"},
    )

    spec.components.schema(
        "HealthStatus",
        {
            "type": "object",
            "properties": {
                "status": {"type": "string", "example": "healthy"},
            },
        },
    )

    spec.components.schema(
        "Student",
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "readOnly": True, "example": 1},
                "name": {"type": "string", "example": "Alice"},
                "age": {"type": "integer", "example": 21},
            },
        },
    )

    spec.components.schema(
        "CreateStudentRequest",
        {
            "type": "object",
            "required": ["name", "age"],
            "properties": {
                "name": {"type": "string", "example": "Alice"},
                "age": {"type": "integer", "example": 21},
            },
        },
    )

    spec.components.schema(
        "UpdateStudentRequest",
        {
            "type": "object",
            "properties": {
                "name": {"type": "string", "example": "Alice Cooper"},
                "age": {"type": "integer", "example": 22},
            },
        },
    )

    spec.components.schema(
        "Error",
        {
            "type": "object",
            "properties": {
                "error": {"type": "string"},
            },
        },
    )

    spec.components.schema(
        "Message",
        {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Student deleted successfully",
                },
            },
        },
    )

    health_status = _ref("HealthStatus")

    spec.path(
        path="/health",
        operations={
            "get": {
                "summary": "Health check",
                "description": "Returns the overall health status of the API.",
                "tags": ["health"],
                "responses": {
                    "200": {
                        "description": "API is healthy.",
                        **_json(health_status),
                    },
                },
            },
        },
    )

    spec.path(
        path="/livez",
        operations={
            "get": {
                "summary": "Liveness check",
                "description": "Returns whether the API process is alive.",
                "tags": ["health"],
                "responses": {
                    "200": {
                        "description": "Process is alive.",
                        **_json(health_status),
                    },
                },
            },
        },
    )

    spec.path(
        path="/readyz",
        operations={
            "get": {
                "summary": "Readiness check",
                "description": (
                    "Returns whether the API is ready to serve traffic"
                    " (database reachable)."
                ),
                "tags": ["health"],
                "responses": {
                    "200": {
                        "description": "Database is reachable.",
                        **_json(health_status),
                    },
                    "503": {
                        "description": "Database is not reachable.",
                        **_json(health_status),
                    },
                },
            },
        },
    )

    student = _ref("Student")
    error = _ref("Error")
    message = _ref("Message")

    spec.path(
        path="/api/v1/students",
        operations={
            "get": {
                "summary": "List all students",
                "description": "Retrieves all student records.",
                "tags": ["students"],
                "responses": {
                    "200": {
                        "description": "Array of student objects.",
                        "content": {
                            "application/json": {
                                "schema": {"type": "array", "items": student},
                            },
                        },
                    },
                },
            },
            "post": {
                "summary": "Create a student",
                "description": "Creates a new student record.",
                "tags": ["students"],
                "requestBody": {
                    "required": True,
                    **_json(_ref("CreateStudentRequest")),
                },
                "responses": {
                    "201": {
                        "description": "Student created successfully.",
                        **_json(student),
                    },
                    "400": {
                        "description": "Invalid input or missing required fields.",
                        **_json(error),
                    },
                },
            },
        },
    )

    spec.path(
        path="/api/v1/students/{student_id}",
        parameters=[
            {
                "name": "student_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
            },
        ],
        operations={
            "get": {
                "summary": "Get a student",
                "description": "Retrieves a specific student by ID.",
                "tags": ["students"],
                "responses": {
                    "200": {"description": "Student details.", **_json(student)},
                    "404": {"description": "Student not found.", **_json(error)},
                },
            },
            "put": {
                "summary": "Update a student",
                "description": "Updates fields of an existing student.",
                "tags": ["students"],
                "requestBody": {
                    "required": True,
                    **_json(_ref("UpdateStudentRequest")),
                },
                "responses": {
                    "200": {
                        "description": "Student updated successfully.",
                        **_json(student),
                    },
                    "400": {
                        "description": "Invalid JSON payload or validation error.",
                        **_json(error),
                    },
                    "404": {"description": "Student not found.", **_json(error)},
                },
            },
            "delete": {
                "summary": "Delete a student",
                "description": "Deletes a student from the database.",
                "tags": ["students"],
                "responses": {
                    "200": {
                        "description": "Student deleted successfully.",
                        **_json(message),
                    },
                    "404": {"description": "Student not found.", **_json(error)},
                },
            },
        },
    )

    return spec


def main():
    parser = argparse.ArgumentParser(description="Generate the OpenAPI specification.")
    parser.add_argument("version", help="API version to write into openapi.json")
    args = parser.parse_args()

    output_path = Path(__file__).resolve().parents[1] / "openapi.json"
    output = json.dumps(build_spec(args.version).to_dict(), indent=2) + "\n"
    output_path.write_text(output)
    print(f"openapi.json written to {output_path}")


if __name__ == "__main__":
    main()

"""Checks on the data coming in from a POST.

Kept out of the view so the view just has to catch TodoValidationError and
turn it into a 400.
"""

MAX_DESCRIPTION_LENGTH = 500


class TodoValidationError(Exception):
    """Raised when a posted todo doesn't pass the checks below."""


def validate_todo_payload(payload) -> str:
    """Check the payload and return the trimmed description.

    Raises TodoValidationError if the body isn't an object, or the
    description is missing, blank, or too long.
    """
    if not isinstance(payload, dict):
        raise TodoValidationError("Request body must be a JSON object.")

    description = payload.get("description")
    if not isinstance(description, str) or not description.strip():
        raise TodoValidationError(
            "Field 'description' is required and cannot be empty."
        )

    description = description.strip()
    if len(description) > MAX_DESCRIPTION_LENGTH:
        raise TodoValidationError(
            f"Field 'description' must be at most "
            f"{MAX_DESCRIPTION_LENGTH} characters."
        )
    return description

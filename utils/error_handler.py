# app/utils/error_handler.py
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from typing import List


def format_validation_errors(errors: List[dict]) -> List[dict]:
    """
    Format Pydantic validation errors to return a consistent error structure.
    """
    formatted_errors = []
    for error in errors:
        field_name = ".".join([str(loc) for loc in error["loc"] if loc != "body"])
        formatted_errors.append({
            "field": field_name,
            "message": error["msg"]
        })
    return formatted_errors


async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Custom exception handler for validation errors globally.
    """
    errors = format_validation_errors(exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "errors": errors},
    )


from pydantic import BaseModel
from fastapi import status,FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import List
class ErrorDetail(BaseModel):
    message:str|List
    success: bool = False
    
class BooklyException(Exception):
    status_code= int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail : ErrorDetail = ErrorDetail(
        message="Internal server error",

    )

class InvalidToken(BooklyException):
    status_code=status.HTTP_401_UNAUTHORIZED ,
    detail = ErrorDetail(
        message="Please obtain a new token"
    )
    

class RevokedToken(BooklyException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ErrorDetail(
        message="Token has been revoked",
    )


class AccessTokenRequired(BooklyException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ErrorDetail(
        message="Valid access token required",

    )


class RefreshTokenRequired(BooklyException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = ErrorDetail(
        message="Valid refresh token required",

    )



class UserAlreadyExists(BooklyException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = ErrorDetail(
        message="User with this email already exists",

    )


class UserNotFound(BooklyException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = ErrorDetail(
        message="User not found",

    )


class AccountNotVerified(BooklyException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = ErrorDetail(
        message="Account not verified,Check your email for the verification link",
    )


# ---- Domain‑specific errors ------------------------------------------------ #
class BookNotFound(BooklyException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = ErrorDetail(
        message="Book not found",

    )


class TagNotFound(BooklyException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = ErrorDetail(
        message="Tag not found",

    )


class TagAlreadyExists(BooklyException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = ErrorDetail(
        message="Tag already exists",

    )


class InvalidCredentials(BooklyException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ErrorDetail(
        message="Invalid email or password",

    )


class InsufficientPermission(BooklyException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ErrorDetail(
        message="You do not have permission to perform this action",

    )
# ---- Review errors ------------------------------------------------- #
class ReviewNotFound(BooklyException):
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ErrorDetail(
        message="Review not found",

    )

def register_all_errors(app: FastAPI):
    @app.exception_handler(BooklyException)
    async def book_exception_handler(request: Request, exc: BooklyException):
        """
            handles BooklyException
        """
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail.model_dump()
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request,exc: RequestValidationError):
        def format_error(error: dict) -> str:
            loc = ".".join(str(item) for item in error.get("loc", []))
            msg = error.get("msg", "")
            ctx = error.get("ctx", {})
            suffix = f" ({ctx.get('error')})" if ctx.get("error") else ""
            return f"{loc}: {msg}{suffix}"
        
        formatted_errors: List[str] = [format_error(err) for err in exc.errors()]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=  ErrorDetail(
                 message=formatted_errors

            ).model_dump()
            

        )   
"""
Native STDERR exceptions to DRF ones
"""

from django.core.exceptions import (
    PermissionDenied,
    ValidationError,
)
from django.db import IntegrityError
from django.db.models.deletion import RestrictedError
from rest_framework import exceptions as rest_exceptions
from rest_framework import status


class APIExceptionCode(rest_exceptions.APIException):

    def __init__(self, status_code, *args, **kwargs):

        self.status_code = status_code
        super().__init__(*args, **kwargs)


class ServiceExceptionHandlerMixin:

    expected_exceptions = {
        AssertionError: rest_exceptions.ParseError,
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied,
        PermissionDenied: rest_exceptions.PermissionDenied,
        IntegrityError: rest_exceptions.ValidationError,
        RestrictedError: rest_exceptions.ValidationError,
        Exception: APIExceptionCode,
    }

    def handle_exception(self, exc):
        if isinstance(
            exc,
            tuple(self.expected_exceptions.keys()),
        ):
            drf_exception_class = (
                self.expected_exceptions.get(
                    exc.__class__,
                    APIExceptionCode,
                )
            )
            drf_exception = (
                drf_exception_class(
                    detail=str(exc),
                    code=status.HTTP_400_BAD_REQUEST,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
                if drf_exception_class == APIExceptionCode
                else drf_exception_class(
                    detail=str(exc),
                    code=status.HTTP_400_BAD_REQUEST,
                )
            )

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)

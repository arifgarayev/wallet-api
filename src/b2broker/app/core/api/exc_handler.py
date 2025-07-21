"""
Native STDERR exceptions to DRF ones
"""

from django.core.exceptions import (
    PermissionDenied,
    ValidationError,
)
from django.db import IntegrityError
from django.db.models.deletion import (
    RestrictedError,
)
from rest_framework import (
    exceptions as rest_exceptions,
)


class ServiceExceptionHandlerMixin:

    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied,
        PermissionDenied: rest_exceptions.PermissionDenied,
        IntegrityError: rest_exceptions.ValidationError,
        RestrictedError: rest_exceptions.ValidationError,
    }

    def handle_exception(self, exc):
        if isinstance(
            exc,
            tuple(
                self.expected_exceptions.keys()
            ),
        ):
            drf_exception_class = self.expected_exceptions[
                exc.__class__
            ]
            drf_exception = (
                drf_exception_class(
                    str(exc)
                )
            )

            return super().handle_exception(
                drf_exception
            )

        return super().handle_exception(
            exc
        )

"""
API views for Transaction Events
"""

from app.common import (
    ServiceExceptionHandlerMixin,
)
from rest_framework.response import (
    Response,
)
from rest_framework.views import APIView


class TransactionCreateApi(
    ServiceExceptionHandlerMixin,
    APIView,
): ...


class TransactionDetailReadApi(
    ServiceExceptionHandlerMixin,
    APIView,
): ...


class TransactionListReadApi(
    ServiceExceptionHandlerMixin,
    APIView,
): ...


class TransactionUpdateApi(
    ServiceExceptionHandlerMixin,
    APIView,
): ...


class TransactionDeleteApi(
    ServiceExceptionHandlerMixin,
    APIView,
): ...

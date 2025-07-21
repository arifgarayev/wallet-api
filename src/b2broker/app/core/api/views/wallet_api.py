"""
API views for Wallet operations
"""

from app.core.api.exc_handler import (
    ServiceExceptionHandlerMixin,
)
from rest_framework.response import (
    Response,
)
from rest_framework.views import APIView


class WalletCreateApi(
    ServiceExceptionHandlerMixin,
    APIView,
): ...

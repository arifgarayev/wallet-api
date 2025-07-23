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
import logging
from app.core.services import (
    WalletService,
    TransactionService,
)
from app.core.api.serializers import (
    WalletCreateInputSerializer,
    WalletCreateOutputSerializer,
    WalletDetailInputSerializer,
    WalletDetailOutputSerializer,
    WalletTransactionOutputSerializer,
    WalletUpdateInputSerializer,
)
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)
from rest_framework import status, mixins, viewsets
from dataclasses import dataclass
from rest_framework_json_api import filters, django_filters
from rest_framework_json_api.pagination import (
    JsonApiPageNumberPagination,
)
from rest_framework import filters as drf_filters


logger = logging.getLogger(__name__)


@dataclass
class WalletApiMeta:
    OPENAPI_TAG = "Transaction"


class TransactionApiBase(
    ServiceExceptionHandlerMixin, APIView
):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wallet_service: TransactionService = (
            TransactionService(view=self)
        )


class BalanceTransactionTopUpApi(TransactionApiBase): ...


class BalanceTransactionDeductApi(TransactionApiBase): ...


class BalanceTransactionWalletToWalletApi(
    TransactionApiBase
): ...

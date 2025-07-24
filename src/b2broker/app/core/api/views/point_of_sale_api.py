"""
API views for Transaction Events
"""

import logging
from dataclasses import dataclass

from app.common import ServiceExceptionHandlerMixin
from app.core.api.serializers import (
    TransactionGenericInputSerializer,
    TransactionGenericOutputSerializer,
)
from app.core.services import TransactionService
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


@dataclass
class POSApiMeta:
    OPENAPI_TAG = "Transaction"


class TransactionApiBase(
    ServiceExceptionHandlerMixin, APIView
):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos_service: TransactionService = (
            TransactionService(view=self)
        )


class BalanceTransactionGenericApi(TransactionApiBase):
    resource_name = "Transaction"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_serializer_cls = (
            TransactionGenericInputSerializer
        )
        self.output_serializer_cls = (
            TransactionGenericOutputSerializer
        )

    def post(self, request):
        raise NotImplementedError


class BalanceTransactionTopUpApi(
    BalanceTransactionGenericApi
):

    @extend_schema(
        tags=[POSApiMeta.OPENAPI_TAG],
        summary="Top-up existing Wallet's Balance",
        request=TransactionGenericInputSerializer,
        responses=TransactionGenericOutputSerializer,
    )
    def post(self, request):
        serialized_model = (
            self.pos_service.balance_standalone_operation(
                request=request
            )
        )

        return Response(
            serialized_model.data,
            status=status.HTTP_201_CREATED,
        )


class BalanceTransactionDeductApi(
    BalanceTransactionGenericApi
):

    @extend_schema(
        tags=[POSApiMeta.OPENAPI_TAG],
        summary="Deduct existing Wallet's Balance if Available",
        request=TransactionGenericInputSerializer,
        responses=TransactionGenericOutputSerializer,
    )
    def post(self, request):
        serialized_model = (
            self.pos_service.balance_standalone_operation(
                request=request, is_deduction=True
            )
        )

        return Response(
            serialized_model.data,
            status=status.HTTP_201_CREATED,
        )


class BalanceTransactionWalletToWalletTransferApi(
    BalanceTransactionGenericApi
):

    @extend_schema(
        tags=[POSApiMeta.OPENAPI_TAG],
        summary="Wallet to Wallet fund movements",
        request=TransactionGenericInputSerializer,
        responses=TransactionGenericOutputSerializer,
    )
    def post(self, request):
        serialized_transactions = (
            self.pos_service.wallet_to_wallet_transfer(
                request
            )
        )
        return Response(
            serialized_transactions.data,
            status=status.HTTP_201_CREATED,
        )

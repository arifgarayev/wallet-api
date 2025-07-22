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
import logging
from app.core.services import (
    WalletService,
)
from app.core.api.serializers import (
    WalletCreateInputSerializer,
    WalletCreateOutputSerializer,
)
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)
from rest_framework import status


logger = logging.getLogger(__name__)


class WalletCreateApi(
    ServiceExceptionHandlerMixin,
    APIView,
):
    """POST request for Wallet creation operation"""

    OPENAPI_TAG = "Wallet"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_serializer: type = (
            WalletCreateInputSerializer
        )
        self.output_serializer: type = (
            WalletCreateOutputSerializer
        )

        self.wallet_service: WalletService = WalletService(
            view=self
        )

    @extend_schema(
        tags=[OPENAPI_TAG],
        request=WalletCreateInputSerializer,
        responses=WalletCreateOutputSerializer,
    )
    def post(self, request):
        output = self.wallet_service.create_wallet(request)
        return Response(
            output.data, status=status.HTTP_201_CREATED
        )


class WalletDetailReadApi(
    ServiceExceptionHandlerMixin,
    APIView,
): ...


class WalletListReadApi(
    ServiceExceptionHandlerMixin,
    APIView,
): ...


class WalletUpdateApi(
    ServiceExceptionHandlerMixin,
    APIView,
): ...


class WalletDeleteApi(
    ServiceExceptionHandlerMixin,
    APIView,
): ...

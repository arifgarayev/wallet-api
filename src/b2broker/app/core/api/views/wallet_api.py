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
    WalletDetailInputSerializer,
    WalletDetailOutputSerializer,
)
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)
from rest_framework import status
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class WalletApiMeta:
    OPENAPI_TAG = "Wallet"


class WalletApiBase(ServiceExceptionHandlerMixin, APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wallet_service: WalletService = WalletService(
            view=self
        )


class WalletCreateApi(WalletApiBase):
    """POST request for Wallet creation operation"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_serializer: type = (
            WalletCreateInputSerializer
        )
        self.output_serializer: type = (
            WalletCreateOutputSerializer
        )

    def get_serializer(self, *args, **kwargs):
        return self.input_serializer

    @extend_schema(
        tags=[WalletApiMeta.OPENAPI_TAG],
        summary="Create Wallet resource",
        request=WalletCreateInputSerializer,
        responses=WalletCreateOutputSerializer,
    )
    def post(self, request):
        output = self.wallet_service.create_wallet(request)
        return Response(
            output.data, status=status.HTTP_201_CREATED
        )


class WalletDetailReadApi(WalletApiBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_serializer = WalletDetailInputSerializer
        self.output_serializer = (
            WalletDetailOutputSerializer
        )

    @extend_schema(
        tags=[WalletApiMeta.OPENAPI_TAG],
        summary="Get Wallet resource by ID",
        request=WalletDetailInputSerializer,
        responses=WalletDetailOutputSerializer,
    )
    def get(self, request, pk):
        output = (
            self.wallet_service.get_wallet_resource_details(
                request, pk=pk
            )
        )
        return Response(
            output.data, status=status.HTTP_201_CREATED
        )


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

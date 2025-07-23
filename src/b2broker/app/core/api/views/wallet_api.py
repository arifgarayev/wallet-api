"""
API views for Wallet operations
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
    OPENAPI_TAG = "Wallet"


class WalletApiBase(ServiceExceptionHandlerMixin, APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wallet_service: WalletService = WalletService(
            view=self
        )


class WalletCreateApi(WalletApiBase):
    """POST request for Wallet creation operation"""

    resource_name = "Wallet"

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
    """GET request for single Wallet resource"""

    resource_name = "Wallet"

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
        print("PK= ", pk)
        output = (
            self.wallet_service.get_wallet_resource_details(
                request, pk=pk
            )
        )
        return Response(
            output.data, status=status.HTTP_200_OK
        )


class WalletListReadApi(WalletApiBase):
    """GET request for list of Wallets with filtering"""

    resource_name = "Wallet"
    paginator = JsonApiPageNumberPagination

    filter_backends = [
        filters.QueryParameterValidationFilter,
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    ]
    ordering_fields = [
        "id",
        "balance",
        "created_at",
        "updated_at",
    ]
    ordering = ["id"]

    filterset_fields = {
        "id": ("exact", "in"),
        "label": (
            "exact",
            "icontains",
            "iexact",
            "contains",
        ),
        "balance": (
            "exact",
            "lt",
            "gt",
            "gte",
            "lte",
        ),
    }

    search_fields = (
        "id",
        "label",
        "balance",
    )

    def filter_queryset(self, queryset):
        for filter in self.filter_backends:
            queryset = filter().filter_queryset(
                self.request, queryset, self
            )

        return queryset

    def get_queryset(self):
        return (
            self.wallet_service.WALLET_MODEL.objects.all()
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_serializer: type = (
            WalletDetailOutputSerializer
        )

    @extend_schema(
        tags=[WalletApiMeta.OPENAPI_TAG],
        summary="Get list of Wallet resources",
        responses=WalletDetailOutputSerializer,
    )
    def get(self, request):
        output = self.wallet_service.get_list(request)

        return output


class WalletListRelatedTransactionsApi(WalletApiBase):
    """GET list of Related Transactions for a single Wallet"""

    resource_name = "Wallet"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_serializer = WalletDetailInputSerializer
        self.output_serializer = (
            WalletTransactionOutputSerializer
        )

    @extend_schema(
        tags=[WalletApiMeta.OPENAPI_TAG],
        summary="Get list of Transactions of a Wallet by ID",
        request=WalletDetailInputSerializer,
        responses=WalletTransactionOutputSerializer,
    )
    def get(self, request, pk):
        output = self.wallet_service.get_and_relate(
            request, pk=pk
        )

        return Response(
            output.data, status=status.HTTP_200_OK
        )


class WalletUpdateApi(WalletApiBase):
    """PATCH for Wallet label update"""

    resource_name = "Wallet"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_serializer = WalletUpdateInputSerializer
        self.output_serializer = (
            WalletTransactionOutputSerializer
        )
        self.payload_serializer = (
            WalletUpdateInputSerializer
        )

    @extend_schema(
        tags=[WalletApiMeta.OPENAPI_TAG],
        summary="Update Wallet label by ID",
        request=WalletUpdateInputSerializer,
        responses=WalletDetailOutputSerializer,
    )
    def patch(self, request, pk):
        output = self.wallet_service.get_and_update(
            request, pk=pk
        )

        return Response(
            output.data, status=status.HTTP_200_OK
        )

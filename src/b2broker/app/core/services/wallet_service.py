from app.core.models import Wallet
from rest_framework.views import APIView
from django.http import HttpRequest
from rest_framework import serializers
from typing import Dict
from django.db import transaction
from django.shortcuts import get_object_or_404
from app.core.api.views import wallet_api
from logging import getLogger


logger = getLogger(__name__)


class WalletService:

    WALLET_MODEL = Wallet

    def __init__(self, *, view):
        self.view: wallet_api.WalletApiBase = view

    def create_wallet(self, request) -> Wallet:
        validated_data = self._validate_creation(
            incoming_data=request.data
        )

        wallet = self._create(validated_data=validated_data)

        serialized_output = self._prepare_response(wallet)

        return serialized_output

    def _prepare_response(self, model):
        return self.view.output_serializer(model)

    @transaction.atomic
    def _create(self, validated_data):
        return self.WALLET_MODEL.objects.create(
            **validated_data
        )

    def _validate_creation(
        self, incoming_data: dict
    ) -> Dict | Exception:
        assert hasattr(
            self.view,
            "input_serializer",
        ), f"Please initialize input_serializer in {self.view.__class__}"

        validated_data: serializers.Serializer = (
            self.view.input_serializer(data=incoming_data)
        )
        validated_data.is_valid(raise_exception=True)
        return validated_data.validated_data

    def get_wallet_resource_details(
        self, request, **kwargs
    ):
        pk = kwargs.get("pk", 0)
        validated_data = self._validate_query_params(
            query_params={"pk": pk}
        )

        wallet_model = get_object_or_404(
            self.WALLET_MODEL,
            id=validated_data.get("pk"),
        )

        return self._prepare_response(wallet_model)

    def _validate_query_params(self, query_params: dict):
        pk = query_params.get("pk", 0)

        if not pk or pk < 0:
            raise ValueError("Invalid ID for Wallet")

        validated_query_param = self.view.input_serializer(
            data=query_params
        )
        validated_query_param.is_valid(raise_exception=True)

        return validated_query_param.validated_data

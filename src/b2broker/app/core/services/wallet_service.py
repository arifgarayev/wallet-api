from app.core.models import Wallet
from rest_framework.views import APIView
from django.http import HttpRequest
from rest_framework import serializers
from typing import Dict
from django.db import transaction


class WalletService:

    WALLET_MODEL = Wallet

    def __init__(self, *, view):
        self.view = view

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
            self.view.input_serializer(incoming_data)
        )
        validated_data.is_valid(raise_exception=True)
        return validated_data.validated_data

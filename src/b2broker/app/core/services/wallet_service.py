from app.core.models import Wallet, PointOfSale
from rest_framework.views import APIView
from django.http import HttpRequest
from rest_framework import serializers
from typing import Dict
from django.db import transaction
from django.shortcuts import get_object_or_404
from app.core.api.views import wallet_api
from logging import getLogger
from rest_framework.response import (
    Response,
)
from app.common import CommonUtils

logger = getLogger(__name__)


class WalletService:

    WALLET_MODEL = Wallet
    BACK_REF_RELATED_MODEL = PointOfSale

    def __init__(self, *, view):
        self.view: wallet_api.WalletApiBase = view

    @transaction.atomic
    def create_wallet(self, request) -> Wallet:
        validated_data = self._validate_creation(
            incoming_data=request.data
        )

        balance = validated_data.pop("balance", 0)

        wallet = self._create(
            self.WALLET_MODEL, validated_data=validated_data
        )
        locked_wallet = self.WALLET_MODEL.objects.select_for_update().get(
            id=wallet.id
        )
        transaction = self._complete_transaction_if_needed(
            locked_wallet, balance
        )

        serialized_output = self._prepare_response(
            locked_wallet
        )

        return serialized_output

    def _complete_transaction_if_needed(
        self, wallet_model, balance
    ):

        transaction_model = None

        if balance > 0:
            transaction_model = self._create(
                self.BACK_REF_RELATED_MODEL,
                validated_data={
                    "wallet_id": wallet_model,
                    "amount": balance,
                },
            )
            wallet_model.balance = balance
            wallet_model.save()

        return transaction_model

    def _prepare_response(self, model, is_many=False):
        return self.view.output_serializer(
            model, many=is_many
        )

    def _create(self, model_class, validated_data):
        return model_class.objects.create(**validated_data)

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

        wallet_model = self._validate_and_get(**kwargs)

        return self._prepare_response(wallet_model)

    def get_and_relate(self, request, **kwargs):
        wallet_model = self._validate_and_get(**kwargs)

        return self._prepare_response(wallet_model)

    @transaction.atomic
    def get_and_update(self, request, **kwargs):
        wallet_model = self._validate_and_get(**kwargs)
        serializer = self.view.payload_serializer(
            data=request.data
        )

        validated_data = serializer.is_valid(
            raise_exception=True
        )

        instance, _ = CommonUtils.model_update(
            instance=wallet_model,
            fields=list(
                self.view.input_serializer.fields.keys()
            ),
            data=validated_data,
        )

        return self._prepare_response(model=instance)

    def _validate_and_get(self, **kwargs):
        """
        pk keyword argument is required
        """

        pk = kwargs.get("pk", 0)
        validated_data = self._validate_query_params(
            query_params={"pk": pk}
        )
        wallet_model = get_object_or_404(
            self.WALLET_MODEL,
            id=validated_data.get("pk"),
        )

        return wallet_model

    def _validate_query_params(self, query_params: dict):
        pk = query_params.get("pk", 0)

        if not pk or pk < 0:
            raise ValueError("Invalid ID for Wallet")

        validated_query_param = self.view.input_serializer(
            data=query_params
        )
        validated_query_param.is_valid(raise_exception=True)

        return validated_query_param.validated_data

    def get_list(self, request):
        q = self.view.get_queryset()
        filtered_q = self.view.filter_queryset(queryset=q)

        paginator = self.view.paginator()

        paginated = paginator.paginate_queryset(
            filtered_q, request, view=self.view
        )

        return (
            paginator.get_paginated_response(
                self._prepare_response(
                    paginated, is_many=True
                ).data
            )
            if paginated
            else Response(
                self._prepare_response(
                    filtered_q, is_many=True
                ).data
            )
        )

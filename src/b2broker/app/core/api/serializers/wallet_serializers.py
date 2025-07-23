from rest_framework import serializers
from app.core.misc import (
    MAX_DIGITS,
    MAX_PRECISION,
)
from decimal import Decimal
from app.core.api.serializers import BaseOutputSerializer


class WalletCreateInputSerializer(serializers.Serializer):
    label = serializers.CharField(
        required=True,
        max_length=255,
    )

    balance = serializers.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_PRECISION,
        min_value=Decimal(0.0),
        initial=0.0,
    )

    class Meta:
        resource_name = "Wallet"


class WalletCreateOutputSerializer(BaseOutputSerializer):
    label = serializers.CharField()
    balance = serializers.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_PRECISION,
    )

    class Meta:
        resource_name = "Wallet"


class WalletDetailInputSerializer(serializers.Serializer):
    pk = serializers.IntegerField(
        required=True, min_value=1
    )

    class Meta:
        resource_name = "Wallet"


class WalletDetailOutputSerializer(
    WalletCreateOutputSerializer
):

    class Meta:
        resource_name = "Wallet"


class WalletTransactionOutputSerializer(
    WalletDetailOutputSerializer
):
    class TransactionSerializer(BaseOutputSerializer):
        txid = serializers.UUIDField()
        amount = serializers.DecimalField(
            max_digits=MAX_DIGITS,
            decimal_places=MAX_PRECISION,
        )

        class Meta:
            resource_name = "Transaction"

    transactions = TransactionSerializer(many=True)


class WalletUpdateInputSerializer(serializers.Serializer):
    label = serializers.CharField(
        required=False,
        max_length=255,
    )

    class Meta:
        resource_name = "Wallet"

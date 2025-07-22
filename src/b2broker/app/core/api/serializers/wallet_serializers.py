from rest_framework import serializers
from app.core.misc import (
    MAX_DIGITS,
    MAX_PRECISION,
)
from decimal import Decimal


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
        resource_name = "WalletCreateApi"


class WalletCreateOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()
    balance = serializers.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_PRECISION,
        initial=0.0,
    )

    class Meta:
        resource_name = "WalletCreateApi"


class WalletDetailInputSerializer(serializers.Serializer):
    pk = serializers.IntegerField(
        required=True, min_value=1
    )


class WalletDetailOutputSerializer(
    WalletCreateOutputSerializer
):

    class Meta:
        resource_name = "WalletWalletDetailReadApi"

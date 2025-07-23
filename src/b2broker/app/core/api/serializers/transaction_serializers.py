from rest_framework import serializers
from app.core.misc import (
    MAX_DIGITS,
    MAX_PRECISION,
)
from app.core.api.serializers import (
    WalletCreateOutputSerializer,
)
from decimal import Decimal


class TransactionGenericInputSerializer(
    serializers.Serializer
):
    "Generic Transaction serializer for"

    "standalone Balance operations and"
    "wallet2wallet fund movements"

    origin_wallet_id = serializers.IntegerField(
        required=True, allow_null=False
    )
    destination_wallet_id = serializers.IntegerField(
        required=False, allow_null=True
    )

    amount = serializers.DecimalField(
        required=True,
        allow_null=False,
        min_value=Decimal(0.0),
        max_digits=MAX_DIGITS,
        decimal_places=MAX_PRECISION,
    )

    def validate_amount(self, value):
        if not value > 0:
            raise ValueError(
                f"Invalid amount {value} for balance operations"
                "Should be > 0.00"
            )
        return value

    def validate_destination_wallet_id(self, value):

        return (
            value
            if not self.context.get(
                "skip_destination", False
            )
            else None
        )

    def validate(self, values):
        if values.get("origin_wallet_id", 0) == values.get(
            "destination_wallet_id", 0
        ):
            raise ValueError(
                "Origin and Destination should be distinct values"
            )

        return values

    class Meta:
        resource_name = "Transaction"


class TransactionGenericOutputSerializer(
    serializers.Serializer
):
    txid = serializers.UUIDField()
    amount = serializers.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_PRECISION,
    )
    wallet = WalletCreateOutputSerializer()

    def to_representation(self, instance):

        return super().to_representation(instance)

    class Meta:
        resource_name = "Transaction"

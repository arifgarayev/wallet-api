from rest_framework import serializers
from app.core.misc import (
    MAX_DIGITS,
    MAX_PRECISION,
)
from app.core.api.serializers import (
    WalletCreateOutputSerializer,
)


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
        min_value=0.0,
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

    class Meta:
        resource_name = "Transaction"

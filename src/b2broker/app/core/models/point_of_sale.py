from app.core.models.base import (
    Timestamped,
    DecimalCustom,
)
from django.db import models
from django.contrib.postgres.functions import (
    RandomUUID,
)
from django.db.models.expressions import (
    RawSQL,
)


class PointOfSale(Timestamped):

    # should not be pkey, so overwrite
    id = models.PositiveIntegerField(
        null=False,
        unique=True,
    )

    wallet_id = models.ForeignKey(
        to="core.Wallet",
        on_delete=models.SET_NULL,
        related_name="transactions",
        null=True,
        help_text="Foreign key to wallet",
    )

    txid = models.UUIDField(
        primary_key=True,
        unique=True,
        db_default=RandomUUID(),
        editable=False,
    )

    amount = DecimalCustom(
        help_text="Transction amount could be negative and positive, should not exceed Wallet's total balance amount",
    )

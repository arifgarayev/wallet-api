from app.core.models.base import DecimalCustom, Timestamped
from django.contrib.postgres.functions import RandomUUID
from django.db import models


class PointOfSale(Timestamped):

    # should not be pkey, so overwrite
    id = None

    wallet = models.ForeignKey(
        to="core.Wallet",
        on_delete=models.PROTECT,
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

    def save(self, *args, **kwargs):
        super().full_clean()
        return super().save(*args, **kwargs)

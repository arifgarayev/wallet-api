from django.db import migrations
from app.core.misc import (
    MAX_DIGITS,
    MAX_PRECISION,
)
from django.db import models


class TimestampedQuerySet(models.QuerySet):
    pass


class Timestamped(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(
        auto_now=True, null=True
    )

    objects = TimestampedQuerySet.as_manager()

    class Meta:
        abstract = True


class DecimalCustom(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "decimal_places",
            MAX_PRECISION,
        )
        kwargs.setdefault(
            "max_digits",
            MAX_DIGITS,
        )

        super().__init__(*args, **kwargs)

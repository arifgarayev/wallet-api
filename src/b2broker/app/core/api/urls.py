from app.core.api.views import (
    WalletCreateApi,
    WalletDetailReadApi,
    WalletListReadApi,
    WalletListRelatedTransactionsApi,
    WalletUpdateApi,
)
from django.urls import path

urlpatterns = [
    path("wallet/create", WalletCreateApi.as_view()),
    path("wallet/<int:pk>", WalletDetailReadApi.as_view()),
    path(
        "wallet/list",
        WalletListReadApi.as_view(),
    ),
    path(
        "wallet/<int:pk>/transactions",
        WalletListRelatedTransactionsApi.as_view(),
    ),
    path(
        "wallet/<int:pk>/update",
        WalletUpdateApi.as_view(),
    ),
]

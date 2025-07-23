from app.core.api.views import (
    WalletCreateApi,
    WalletDetailReadApi,
    WalletListReadApi,
    WalletListRelatedTransactionsApi,
    WalletUpdateApi,
    BalanceTransactionTopUpApi,
    BalanceTransactionDeductApi,
    BalanceTransactionWalletToWalletTransferApi,
)
from django.urls import path

WALLET_URLs = [
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


POS_URLs = [
    path(
        "transaction/top-up",
        BalanceTransactionTopUpApi.as_view(),
    ),
    path(
        "transaction/deduct",
        BalanceTransactionDeductApi.as_view(),
    ),
    path(
        "transaction/move-funds",
        BalanceTransactionWalletToWalletTransferApi.as_view(),
    ),
]

urlpatterns = WALLET_URLs + POS_URLs

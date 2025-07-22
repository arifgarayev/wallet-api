from app.core.api.views import (
    WalletCreateApi,
    WalletDetailReadApi,
)
from django.urls import path

urlpatterns = [
    path("wallet/create", WalletCreateApi.as_view()),
    path("wallet/<int:pk>", WalletDetailReadApi.as_view()),
]

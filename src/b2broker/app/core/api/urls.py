from app.core.api.views import WalletCreateApi
from django.urls import path

urlpatterns = [
    path("wallet/create", WalletCreateApi.as_view()),
]

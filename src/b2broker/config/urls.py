from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/schema/",
        SpectacularAPIView.as_view(api_version="v1"),
        name="schema_v1",
    ),
    path(
        "",
        SpectacularSwaggerView.as_view(
            url_name="schema_v1"
        ),
        name="swagger-ui",
    ),
    path(
        "api/v1/",
        include(
            [path("core/", include("app.core.api.urls"))]
        ),
    ),
]

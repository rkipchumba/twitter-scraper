from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Configuration
swagger_info = openapi.Info(
    title="Twitter Scraper API",
    default_version='v1',
    description="API documentation for the Twitter Scraper",
    terms_of_service="https://www.example.com/policies/terms/",
    contact=openapi.Contact(email="contact@example.com"),
    license=openapi.License(name="BSD License"),
)

schema_view = get_schema_view(
    swagger_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# URL Configuration
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('scraper.urls')),  # Prefix API endpoints with 'api/'
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Default view for root URL
]

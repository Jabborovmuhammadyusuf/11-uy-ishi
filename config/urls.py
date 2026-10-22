from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(
    title="Kitoblar API",
    description="Janrlar, kitoblar va izohlar API hujjati",
    version="1.0.0",
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('schema/', schema_view, name='openapi-schema'),
    path('swagger/', TemplateView.as_view(template_name='swagger-ui.html', extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

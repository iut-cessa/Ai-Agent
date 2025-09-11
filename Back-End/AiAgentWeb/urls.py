"""
URL configuration for AiAgentWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import AuthenticatedSwaggerView, AuthenticatedRedocView, swagger_login_redirect, swagger_logout_redirect

# Swagger/OpenAPI schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="AI Agent API",
        default_version='v1',
        description="API documentation for AI Agent Web Application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@aiagent.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,  # Changed to False to require authentication
    permission_classes=(permissions.IsAuthenticated,),  # Require authentication
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/user/', include('account.urls')),
    path('api/course/', include('course.urls')),
    
    # Authentication URLs for Swagger
    path('swagger-login/', swagger_login_redirect, name='swagger-login'),
    path('swagger-logout/', swagger_logout_redirect, name='swagger-logout'),
    
    # API Documentation - Now requires authentication
    path('', AuthenticatedSwaggerView.as_view(), name='schema-swagger-ui'),
    path('swagger/', AuthenticatedSwaggerView.as_view(), name='schema-swagger-ui-auth'),
    path('redoc/', AuthenticatedRedocView.as_view(), name='schema-redoc-auth'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    
    # DRF API Browser
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .spectacular_views import (
    AuthenticatedSpectacularAPIView,
    AuthenticatedSpectacularSwaggerView,
    AuthenticatedSpectacularRedocView,
    api_root_view
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/user/', include('account.urls')),
    path('api/course/', include('course.urls')),
    
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # API Documentation (requires authentication)
    path('schema/', AuthenticatedSpectacularAPIView.as_view(), name='schema'),
    path('', api_root_view, name='api-root'),
    path('swagger/', AuthenticatedSpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', AuthenticatedSpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # DRF API Browser
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


# Custom schema view that requires authentication
schema_view_authenticated = get_schema_view(
    openapi.Info(
        title="AI Agent API",
        default_version='v1',
        description="API documentation for AI Agent Web Application - Authentication Required",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@aiagent.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)


class AuthenticatedSwaggerView(LoginRequiredMixin, TemplateView):
    """
    Custom Swagger view that requires user authentication
    """
    login_url = '/admin/login/'
    
    def get(self, request, *args, **kwargs):
        # If user is authenticated, show swagger
        if request.user.is_authenticated:
            return schema_view_authenticated.with_ui('swagger', cache_timeout=0)(request, *args, **kwargs)
        else:
            # Redirect to login page
            return redirect(self.login_url)


class AuthenticatedRedocView(LoginRequiredMixin, TemplateView):
    """
    Custom Redoc view that requires user authentication
    """
    login_url = '/admin/login/'
    
    def get(self, request, *args, **kwargs):
        # If user is authenticated, show redoc
        if request.user.is_authenticated:
            return schema_view_authenticated.with_ui('redoc', cache_timeout=0)(request, *args, **kwargs)
        else:
            # Redirect to login page
            return redirect(self.login_url)


# Create a simple login view that redirects to Django admin login
def swagger_login_redirect(request):
    """Redirect to Django admin login for Swagger authentication"""
    return redirect('/admin/login/')


def swagger_logout_redirect(request):
    """Logout and redirect to home"""
    return auth_views.LogoutView.as_view(next_page='/')(request)

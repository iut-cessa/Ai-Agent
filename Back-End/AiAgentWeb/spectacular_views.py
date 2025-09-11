"""
Custom authenticated views for DRF Spectacular API documentation
"""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


class AuthenticatedSpectacularAPIView(SpectacularAPIView):
    """
    API schema view that requires authentication
    """
    permission_classes = [permissions.IsAuthenticated]


@method_decorator(login_required, name='dispatch')
class AuthenticatedSpectacularSwaggerView(SpectacularSwaggerView):
    """
    Swagger UI view that requires authentication
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class AuthenticatedSpectacularRedocView(SpectacularRedocView):
    """
    ReDoc view that requires authentication
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_root_view(request):
    """
    Root API view that shows available endpoints for authenticated users
    """
    return Response({
        'message': 'Welcome to AI Agent API',
        'user': request.user.username if request.user.is_authenticated else 'Anonymous',
        'endpoints': {
            'swagger': request.build_absolute_uri('/swagger/'),
            'redoc': request.build_absolute_uri('/redoc/'),
            'schema': request.build_absolute_uri('/schema/'),
            'api': {
                'user': request.build_absolute_uri('/api/user/'),
                'course': request.build_absolute_uri('/api/course/'),
            }
        }
    })

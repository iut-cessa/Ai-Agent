from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from account.renderers import UserRenderer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [AllowAny]  # Allow registration without authentication
  
  @extend_schema(
      summary="User Registration",
      description="Register a new user account",
      request=UserRegistrationSerializer,
      responses={
          201: {
              "description": "Registration successful",
              "example": {
                  "token": {
                      "refresh": "refresh_token_here",
                      "access": "access_token_here"
                  },
                  "msg": "Registration Success"
              }
          },
          400: {"description": "Bad request - validation errors"},
      },
      tags=['User - Authentication']
  )
  def post(self,request,format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token,'msg':'Registration Success'},status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [AllowAny]  # Allow login without authentication
  
  @extend_schema(
      summary="User Login",
      description="Authenticate user and get JWT tokens",
      request=UserLoginSerializer,
      responses={
          200: {
              "description": "Login successful",
              "example": {
                  "token": {
                      "refresh": "refresh_token_here",
                      "access": "access_token_here"
                  },
                  "msg": "Login Success"
              }
          },
          404: {"description": "Invalid credentials"},
          400: {"description": "Bad request - validation errors"},
      },
      tags=['User - Authentication']
  )
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  
  @extend_schema(
      summary="Get User Profile",
      description="Get current authenticated user's profile information",
      responses={
          200: UserProfileSerializer,
          401: {"description": "Unauthorized - Authentication required"},
      },
      tags=['User - Profile Management']
  )
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  
  @extend_schema(
      summary="Change Password",
      description="Change password for authenticated user",
      request=UserChangePasswordSerializer,
      responses={
          200: {
              "description": "Password changed successfully",
              "example": {
                  "msg": "Password Changed Successfully"
              }
          },
          400: {"description": "Bad request - validation errors"},
          401: {"description": "Unauthorized - Authentication required"},
      },
      tags=['User - Profile Management']
  )
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

  
class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [AllowAny]  # Allow password reset email without authentication
  
  @extend_schema(
      summary="Send Password Reset Email",
      description="Send password reset link to user's email",
      request=SendPasswordResetEmailSerializer,
      responses={
          200: {
              "description": "Password reset email sent",
              "example": {
                  "msg": "Password Reset link send. Please check your Email"
              }
          },
          400: {"description": "Bad request - validation errors"},
      },
      tags=['User - Password Reset']
  )
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [AllowAny]  # Allow password reset without authentication
  
  @extend_schema(
      summary="Reset Password",
      description="Reset user password using token from email",
      request=UserPasswordResetSerializer,
      parameters=[
          OpenApiParameter('uid', OpenApiTypes.STR, OpenApiParameter.PATH, description="User ID"),
          OpenApiParameter('token', OpenApiTypes.STR, OpenApiParameter.PATH, description="Reset token"),
      ],
      responses={
          200: {
              "description": "Password reset successful",
              "example": {
                  "msg": "Password Reset Successfully"
              }
          },
          400: {"description": "Bad request - validation errors"},
      },
      tags=['User - Password Reset']
  )
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

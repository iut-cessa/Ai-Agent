from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from account.renderers import UserRenderer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [AllowAny]  # Allow registration without authentication
  
  @swagger_auto_schema(
      operation_summary="User Registration",
      operation_description="Register a new user account",
      request_body=UserRegistrationSerializer,
      responses={
          201: openapi.Response(
              description="Registration successful",
              examples={
                  "application/json": {
                      "token": {
                          "refresh": "refresh_token_here",
                          "access": "access_token_here"
                      },
                      "msg": "Registration Success"
                  }
              }
          ),
          400: openapi.Response("Bad request - validation errors"),
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
  
  @swagger_auto_schema(
      operation_summary="User Login",
      operation_description="Authenticate user and get JWT tokens",
      request_body=UserLoginSerializer,
      responses={
          200: openapi.Response(
              description="Login successful",
              examples={
                  "application/json": {
                      "token": {
                          "refresh": "refresh_token_here",
                          "access": "access_token_here"
                      },
                      "msg": "Login Success"
                  }
              }
          ),
          404: openapi.Response("Invalid credentials"),
          400: openapi.Response("Bad request - validation errors"),
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
  
  @swagger_auto_schema(
      operation_summary="Get User Profile",
      operation_description="Get current authenticated user's profile information",
      responses={
          200: UserProfileSerializer,
          401: openapi.Response("Unauthorized - Authentication required"),
      },
      tags=['User - Profile Management'],
      security=[{'Bearer': []}]
  )
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  
  @swagger_auto_schema(
      operation_summary="Change Password",
      operation_description="Change password for authenticated user",
      request_body=UserChangePasswordSerializer,
      responses={
          200: openapi.Response(
              description="Password changed successfully",
              examples={
                  "application/json": {
                      "msg": "Password Changed Successfully"
                  }
              }
          ),
          400: openapi.Response("Bad request - validation errors"),
          401: openapi.Response("Unauthorized - Authentication required"),
      },
      tags=['User - Profile Management'],
      security=[{'Bearer': []}]
  )
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

  
class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [AllowAny]  # Allow password reset email without authentication
  
  @swagger_auto_schema(
      operation_summary="Send Password Reset Email",
      operation_description="Send password reset link to user's email",
      request_body=SendPasswordResetEmailSerializer,
      responses={
          200: openapi.Response(
              description="Password reset email sent",
              examples={
                  "application/json": {
                      "msg": "Password Reset link send. Please check your Email"
                  }
              }
          ),
          400: openapi.Response("Bad request - validation errors"),
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
  
  @swagger_auto_schema(
      operation_summary="Reset Password",
      operation_description="Reset user password using token from email",
      request_body=UserPasswordResetSerializer,
      manual_parameters=[
          openapi.Parameter('uid', openapi.IN_PATH, description="User ID", type=openapi.TYPE_STRING),
          openapi.Parameter('token', openapi.IN_PATH, description="Reset token", type=openapi.TYPE_STRING),
      ],
      responses={
          200: openapi.Response(
              description="Password reset successful",
              examples={
                  "application/json": {
                      "msg": "Password Reset Successfully"
                  }
              }
          ),
          400: openapi.Response("Bad request - validation errors"),
      },
      tags=['User - Password Reset']
  )
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

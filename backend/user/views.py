from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .services import OTPService, UserService, ProfileService
from .serializers import (OTPRequestSerializer, 
                          PasswordResetSerializer, 
                          RegisterSerializer, 
                          ProfileSerializer,
                          CustomTokenObtainPairSerializer,)


class RegisterView(APIView):
    """
    An endpoint for Users to register their accounts
    """
    
    def post(self, request):
        data = request.data
        user = UserService.register_user(
        email=data['email'],
        username=data['username'],
        phone=data['phone'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name']
        )
        serializer = RegisterSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    """
    An endpoint for User's to manage their Profiles
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = ProfileService.get_profile(request.user)
        if profile:
            srz = ProfileSerializer(profile)
            return Response(srz.data)
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        profile = ProfileService.get_profile(request.user)
        if profile:
            srz = ProfileSerializer(profile, data=request.data, partial=True)
            if srz.is_valid():
                ProfileService.update_profile(request.user, **srz.validated_data)
                return Response(srz.data)
            return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request):
        if ProfileService.delete_profile(request.user):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    An endpoint for Users to get access token
    """

    serializer_class = CustomTokenObtainPairSerializer


class OTPRequestView(APIView):
    """
    An endpoint to confirm User's emails and send OTP token
    """

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            result = OTPService.request_otp(serializer.validated_data['email'])
            if result['error']:
                return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'otp': result['otp']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """
    An endpoint for Resetting password for Users
    """
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            if OTPService.reset_password(email, otp, new_password):
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

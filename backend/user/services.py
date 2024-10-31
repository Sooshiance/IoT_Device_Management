# services/user_service.py
from django.utils import timezone

import pyotp

from .models import User
from .repositories import UserRepository, ProfileRepository, OTPRepository
from .utils import sendToken


class UserService:
    """
    
    """
    @staticmethod
    def register_user(email, username, phone, password, first_name, last_name):
        user = UserRepository.create_user(
        email=email,
        username=username,
        phone=phone,
        password=password,
        first_name=first_name,
        last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def get_user_by_email(email):
        return UserRepository.get_user_by_email(email)


class ProfileService:
    """
    
    """
    @staticmethod
    def get_profile(user):
        return ProfileRepository.get_profile_by_user(user)
    
    @staticmethod
    def update_profile(user, **kwargs):
        profile = ProfileRepository.get_profile_by_user(user)
        if profile:
            return ProfileRepository.update_profile(profile, **kwargs)
        return None
    
    @staticmethod
    def delete_profile(user):
        profile = ProfileRepository.get_profile_by_user(user)
        if profile:
            ProfileRepository.delete_profile(profile)
            return True
        return False


class OTPService:
    """
    
    """
    @staticmethod
    def request_otp(email):
        try:
            user = User.objects.get(email=email)
            result = sendToken(user)
            return result
        except User.DoesNotExist:
            return {'error': 'User not found', 'otp': False}
    
    @staticmethod
    def verify_otp(email, otp):
        try:
            user = User.objects.get(email=email)
            otp_record = OTPRepository.get_otp_by_user(user)
            if (timezone.now() - otp_record.created_at).seconds < 60:
                otp_record.delete()
            if otp_record and otp_record.otp == otp and (timezone.now() - otp_record.created_at).seconds < 60:
                return True
            return False
        except User.DoesNotExist:
            return False

    @staticmethod
    def reset_password(email, otp, new_password):
        if OTPService.verify_otp(email, otp):
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            OTPRepository.delete_otp_by_user(user)
            return True
        return False

from .models import User, Profile, OTP


class UserRepository:
    """
    
    """
    @staticmethod
    def get_user_by_email(email)-> User:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    @staticmethod
    def create_user(**kwargs)-> User:
        user:User = User.objects.create_user(**kwargs)
        return user

    @staticmethod
    def update_user(user, **kwargs):
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user


class ProfileRepository:
    """
    
    """
    @staticmethod
    def get_profile_by_user(user):
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return None

    @staticmethod
    def update_profile(profile, **kwargs):
        for key, value in kwargs.items():
            setattr(profile, key, value)
            profile.save()
            return profile

    @staticmethod
    def delete_profile(profile):
        profile.delete()


class OTPRepository:
    """
    
    """
    @staticmethod
    def get_otp_by_user(user):
        try:
            return OTP.objects.get(user=user)
        except OTP.DoesNotExist:
            return None

    @staticmethod
    def delete_otp_by_user(user):
        OTP.objects.filter(user=user).delete()

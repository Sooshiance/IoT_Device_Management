import datetime
from django.utils import timezone

import pyotp

from .models import OTP


def sendToken(user):

    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)

    otp = totp.now()

    OTP.objects.create(user=user, otp=otp).save()

    print(f"OTP ====== {otp}")

    return {'otp': otp, 'error': False}

from rest_framework import serializers

from .models import (Device,
                     DeviceGroup,
                     DeviceData,
                     DeviceAuditLog,
                     Notification)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class DeviceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceGroup
        fields = "__all__"


class DeviceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceData
        fields = "__all__"


class DeviceAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceAuditLog
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

from django.db import models

from shortuuid.django_fields import ShortUUIDField

from device.enums import DeviceType

from user.models import User


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=DeviceType.choices())
    status = models.BooleanField(default=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    firmware_version = models.CharField(max_length=50, null=True, blank=True)
    last_communication = models.DateTimeField(null=True, blank=True)
    did = ShortUUIDField(max_length=20, db_index=True, unique=True, alphabet="0123456789abcdefghij")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class DeviceGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_groups')
    name = models.CharField(max_length=100)
    devices = models.ManyToManyField(Device, related_name='groups')
    gid = ShortUUIDField(max_length=20, db_index=True, unique=True, alphabet="0123456789abcdefghij")

    class Meta:
        verbose_name = 'Device Group'
        verbose_name_plural = 'Device Groups'

    def __str__(self):
        return self.name


class DeviceData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='data_records')
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()
    did = ShortUUIDField(max_length=20, db_index=True, unique=True, alphabet="0123456789abcdefghij")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['device', 'timestamp'], name='unique_device_timestamp')
        ]
        verbose_name = 'Device Data'
        verbose_name_plural = 'Device Data'

    def __str__(self):
        return f"Data for {self.device.name} at {self.timestamp}"


class DeviceAuditLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    details = models.JSONField()
    lid = ShortUUIDField(max_length=20, db_index=True, unique=True, alphabet="0123456789abcdefghij")

    class Meta:
        verbose_name = 'Device Audit Log'
        verbose_name_plural = 'Device Audit Logs'

    def __str__(self):
        return f"{self.action} on {self.device.name} by {self.user} at {self.timestamp}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    nid = ShortUUIDField(max_length=20, db_index=True, unique=True, alphabet="0123456789abcdefghij")

    def __str__(self):
        return f"Notification for {self.user} at {self.created_at}"

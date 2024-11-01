from django.db import transaction

from .models import (Device,
                     DeviceGroup,
                     DeviceData,
                     DeviceAuditLog,
                     Notification)


class DeviceRepository:
    def get_all_devices(self, user):
        return Device.objects.filter(user=user)

    def get_device_by_id(self, user, did):
        return Device.objects.filter(user=user, did=did).first()

    def create_device(self, user, **kwargs):
        with transaction.atomic():
            device = Device.objects.create(user=user, **kwargs)
            return device

    def update_device(self, device, **kwargs):
        for attr, value in kwargs.items():
            setattr(device, attr, value)
        device.save()
        return device

    def delete_device(self, device):
        device.delete()

class DeviceGroupRepository:
    def get_all_device_groups(self, user):
        return DeviceGroup.objects.filter(user=user)

    def get_device_group_by_id(self, user, gid):
        return DeviceGroup.objects.filter(user=user, gid=gid).first()

    def create_device_group(self, user, name):
        group = DeviceGroup.objects.create(user=user, name=name)
        return group

    def add_device_to_group(self, group, device):
        group.devices.add(device)

    def remove_device_from_group(self, group, device):
        group.devices.remove(device)

    def delete_device_group(self, group):
        group.delete()

class DeviceDataRepository:

    def create_device_data(device, data):
        return DeviceData.objects.create(device=device, data=data)

    def get_device_data_by_device(device):
        return DeviceData.objects.filter(device=device).order_by('-timestamp')

    def get_device_data_by_id(data_id):
        return DeviceData.objects.get(did=data_id)

class DeviceAuditLogRepository:

    def create_audit_log(device, action, user, details):
        return DeviceAuditLog.objects.create(device=device, action=action, user=user, details=details)

    def get_audit_logs_by_device(device):
        return DeviceAuditLog.objects.filter(device=device).order_by('-timestamp')

class NotificationRepository:

    def create_notification(user, message):
        return Notification.objects.create(user=user, message=message)

    def get_notifications_for_user(user):
        return Notification.objects.filter(user=user).order_by('-created_at')

    def mark_notification_as_read(notification_id):
        notification = Notification.objects.get(nid=notification_id)
        notification.is_read = True
        notification.save()

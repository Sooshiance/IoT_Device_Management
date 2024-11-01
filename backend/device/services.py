from rest_framework.exceptions import ValidationError

from device.repositories import (DeviceRepository,
                                 DeviceGroupRepository,
                                 DeviceDataRepository,
                                 DeviceAuditLogRepository,
                                 NotificationRepository,)


class DeviceService:
    def __init__(self):
        self.device_repository = DeviceRepository()

    def get_all_devices(self, user):
        return self.device_repository.get_all_devices(user)

    def get_device_by_id(self, user, did):
        device = self.device_repository.get_device_by_id(user, did)
        if not device:
            raise ValidationError(detail="Device not found.")
        return device

    def create_device(self, user, **kwargs):
        return self.device_repository.create_device(user, **kwargs)

    def update_device(self, user, did, **kwargs):
        device = self.device_repository.get_device_by_id(user, did)
        if not device:
            raise ValidationError(detail="Device not found.")
        return self.device_repository.update_device(device, **kwargs)

    def delete_device(self, user, did):
        device = self.device_repository.get_device_by_id(user, did)
        if not device:
            raise ValidationError(detail="Device not found.")
        self.device_repository.delete_device(device)


class DeviceGroupService:
    def __init__(self):
        self.device_group_repository = DeviceGroupRepository()

    def get_all_device_groups(self, user):
        return self.device_group_repository.get_all_device_groups(user)

    def get_device_group_by_id(self, user, gid):
        group = self.device_group_repository.get_device_group_by_id(user, gid)
        if not group:
            raise ValidationError(detail="Device group not found.")
        return group

    def create_device_group(self, user, name):
        return self.device_group_repository.create_device_group(user, name)

    def add_device_to_group(self, user, gid, device):
        group = self.device_group_repository.get_device_group_by_id(user, gid)
        if not group:
            raise ValidationError(detail="Device group not found.")
        self.device_group_repository.add_device_to_group(group, device)

    def remove_device_from_group(self, user, gid, device):
        group = self.device_group_repository.get_device_group_by_id(user, gid)
        if not group:
            raise ValidationError(detail="Device group not found.")
        self.device_group_repository.remove_device_from_group(group, device)

    def delete_device_group(self, user, gid):
        group = self.device_group_repository.get_device_group_by_id(user, gid)
        if not group:
            raise ValidationError(detail="Device group not found.")
        self.device_group_repository.delete_device_group(group)


class DeviceDataService:
    def __init__(self):
        self.device_data_repository = DeviceDataRepository()

    def create_device_data(self, device, data):
        return self.device_data_repository.create_device_data(device, data)

    def get_device_data_by_device(self, device):
        return self.device_data_repository.get_device_data_by_device(device)

    def get_device_data_by_id(self, data_id):
        data = self.device_data_repository.get_device_data_by_id(data_id)
        if not data:
            raise ValidationError(detail="Device data not found.")
        return data


class DeviceAuditLogService:
    def __init__(self):
        self.device_audit_log_repository = DeviceAuditLogRepository()

    def create_audit_log(self, device, action, user, details):
        return self.device_audit_log_repository.create_audit_log(device, action, user, details)

    def get_audit_logs_by_device(self, device):
        return self.device_audit_log_repository.get_audit_logs_by_device(device)


class NotificationService:
    def __init__(self):
        self.notification_repository = NotificationRepository()

    def create_notification(self, user, message):
        return self.notification_repository.create_notification(user, message)

    def get_notifications_for_user(self, user):
        return self.notification_repository.get_notifications_for_user(user)

    def mark_notification_as_read(self, notification_id):
        notification = self.notification_repository.get_notifications_for_user(notification_id)
        if not notification:
            raise ValidationError(detail="Notification not found.")
        return self.notification_repository.mark_notification_as_read(notification_id)

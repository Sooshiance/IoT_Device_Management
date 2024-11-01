from django.contrib import admin

from device.models import (Device,
                           DeviceData,
                           DeviceGroup,
                           DeviceAuditLog,
                           Notification)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['']


class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ['']


class DeviceGroupAdmin(admin.ModelAdmin):
    list_display = ['']


class DeviceAuditLogAdmin(admin.ModelAdmin):
    list_display = ['']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['']


admin.site.register(Device, DeviceAdmin)

admin.site.register(DeviceData, DeviceDataAdmin)

admin.site.register(DeviceGroup, DeviceGroupAdmin)

admin.site.register(DeviceAuditLog, DeviceAuditLogAdmin)

admin.site.register(Notification, NotificationAdmin)

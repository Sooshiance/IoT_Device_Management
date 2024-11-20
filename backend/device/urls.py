from django.urls import path

from .views import (DeviceListCreateAPIView,
                    DeviceRetrieveUpdateDestroyAPIView,
                    DeviceGroupListCreateAPIView,
                    DeviceGroupRetrieveUpdateDestroyAPIView,
                    DeviceDataListCreateAPIView,
                    DeviceAuditLogListAPIView,
                    NotificationListCreateAPIView,
                    NotificationMarkAsReadAPIView,)


app_name = "device"

urlpatterns = [
    path('devices/', DeviceListCreateAPIView.as_view(), name='device-list-create'),
    path('devices/<str:did>/', DeviceRetrieveUpdateDestroyAPIView.as_view(), name='device-detail'),
    path('device-groups/', DeviceGroupListCreateAPIView.as_view(), name='device-group-list-create'),
    path('device-groups/<str:gid>/', DeviceGroupRetrieveUpdateDestroyAPIView.as_view(), name='device-group-detail'),
    path('devices/<str:did>/data/', DeviceDataListCreateAPIView.as_view(), name='device-data-list-create'),
    path('devices/<str:did>/audit-logs/', DeviceAuditLogListAPIView.as_view(), name='device-audit-log-list'),
    path('notifications/', NotificationListCreateAPIView.as_view(), name='notification-list-create'),
    path('notifications/<str:nid>/mark-as-read/', NotificationMarkAsReadAPIView.as_view(), name='notification-mark-as-read'),
]

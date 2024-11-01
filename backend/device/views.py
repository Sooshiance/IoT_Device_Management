from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

# from .models import Device, DeviceGroup, DeviceData, DeviceAuditLog, Notification
from .serializers import (DeviceSerializer, 
                          DeviceGroupSerializer,
                          DeviceDataSerializer, 
                          DeviceAuditLogSerializer,
                          NotificationSerializer)
from .services import (DeviceService,
                       DeviceGroupService,
                       DeviceDataService, 
                       DeviceAuditLogService,
                       NotificationService,)


class DeviceListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return DeviceService().get_all_devices(self.request.user)

    def perform_create(self, serializer):
        DeviceService().create_device(self.request.user, **serializer.validated_data)


class DeviceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer
    lookup_field = 'did'

    def get_queryset(self):
        return DeviceService().get_all_devices(self.request.user)

    def perform_update(self, serializer):
        DeviceService().update_device(self.request.user, self.kwargs['did'], **serializer.validated_data)

    def perform_destroy(self, instance):
        DeviceService().delete_device(self.request.user, self.kwargs['did'])


class DeviceGroupListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DeviceGroupSerializer

    def get_queryset(self):
        return DeviceGroupService().get_all_device_groups(self.request.user)

    def perform_create(self, serializer):
        DeviceGroupService().create_device_group(self.request.user, **serializer.validated_data)


class DeviceGroupRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceGroupSerializer
    lookup_field = 'gid'

    def get_queryset(self):
        return DeviceGroupService().get_all_device_groups(self.request.user)

    def perform_update(self, serializer):
        DeviceGroupService().update_device_group(self.request.user, self.kwargs['gid'], **serializer.validated_data)

    def perform_destroy(self, instance):
        DeviceGroupService().delete_device_group(self.request.user, self.kwargs['gid'])


class DeviceDataListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DeviceDataSerializer

    def get_queryset(self):
        device = DeviceService().get_device_by_id(self.request.user, self.kwargs['did'])
        return DeviceDataService().get_device_data_by_device(device)

    def perform_create(self, serializer):
        device = DeviceService().get_device_by_id(self.request.user, self.kwargs['did'])
        DeviceDataService().create_device_data(device, **serializer.validated_data)


class DeviceAuditLogListAPIView(generics.ListAPIView):
    serializer_class = DeviceAuditLogSerializer

    def get_queryset(self):
        device = DeviceService().get_device_by_id(self.request.user, self.kwargs['did'])
        return DeviceAuditLogService().get_audit_logs_by_device(device)


class NotificationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return NotificationService().get_notifications_for_user(self.request.user)

    def perform_create(self, serializer):
        NotificationService().create_notification(self.request.user, **serializer.validated_data)


class NotificationMarkAsReadAPIView(APIView):
    def post(self, request, nid):
        NotificationService().mark_notification_as_read(nid)
        return Response(status=status.HTTP_204_NO_CONTENT)

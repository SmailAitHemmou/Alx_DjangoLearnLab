from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class ListNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

class UnreadNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user, unread=True).order_by('-timestamp')

class MarkNotificationReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notif.unread = False
        notif.save()
        return Response({'detail': 'Marked as read'}, status=status.HTTP_200_OK)

class MarkAllReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)
        return Response({'detail': 'All marked as read'}, status=status.HTTP_200_OK)

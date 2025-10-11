from django.urls import path
from .views import ListNotificationsView, UnreadNotificationsView, MarkNotificationReadView, MarkAllReadView

urlpatterns = [
    path('', ListNotificationsView.as_view(), name='notifications-list'),
    path('unread/', UnreadNotificationsView.as_view(), name='notifications-unread'),
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-mark-read'),
    path('mark-all-read/', MarkAllReadView.as_view(), name='notifications-mark-all-read'),
]

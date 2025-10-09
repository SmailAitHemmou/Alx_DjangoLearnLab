from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    FollowView, UnfollowView,
    FollowersListView, FollowingListView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnfollowView.as_view(), name='unfollow'),
    path('users/<int:user_id>/followers/', FollowersListView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', FollowingListView.as_view(), name='user-following'),
]

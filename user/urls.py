from django.urls import path
from .views import UserAPIView, UserDeleteAPIView, UserLoginAPIView, UserRangeListAPIView, UserUpdateAPIView

urlpatterns = [
    path('register', UserAPIView.as_view(), name = 'auth_register'),
    path('login', UserLoginAPIView.as_view(), name='auth_login'),
    path('delete', UserDeleteAPIView.as_view(), name='user_delete'),
    path('update', UserUpdateAPIView.as_view(), name='user-update'),
    path('range', UserRangeListAPIView.as_view(), name = 'user-range-list'),
    path('id/<int:pk>', UserAPIView.as_view(), name = 'get-user-by-id')
]
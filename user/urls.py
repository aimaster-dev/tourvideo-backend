from django.urls import path
from .views import UserAPIView, UserDeleteAPIView, UserLoginAPIView, ISPRangeListAPIView, ClientRangeListAPIView, UserUpdateAPIView

urlpatterns = [
    path('register', UserAPIView.as_view(), name = 'auth_register'),
    path('login', UserLoginAPIView.as_view(), name='auth_login'),
    path('delete', UserDeleteAPIView.as_view(), name='user_delete'),
    path('update', UserUpdateAPIView.as_view(), name='user-update'),
    path('isprange', ISPRangeListAPIView.as_view(), name = 'isp-range-list'),
    path('clientrange', ClientRangeListAPIView.as_view(), name = 'client-range-list'),
    path('id/<int:pk>', UserAPIView.as_view(), name = 'get-user-by-id')
]
from django.urls import path
from .views import CameraAPIView, CameraUpdateAPIView, CameraDeleteAPIView

urlpatterns = [
    path('register', CameraAPIView.as_view(), name = 'camera_register'),
    path('getall', CameraAPIView.as_view(), name = 'get_all_camera_of_current_isp'),
    path('update', CameraUpdateAPIView.as_view(), name = 'update_camera'),
    path('delete', CameraUpdateAPIView.as_view(), name = 'delete_camera'),
]
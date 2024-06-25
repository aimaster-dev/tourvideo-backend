from django.urls import path
from .views import CameraAPIView, CameraUpdateAPIView, CameraDeleteAPIView

urlpatterns = [
    path('add', CameraAPIView.as_view(), name = 'camera_add'),
    path('getall', CameraAPIView.as_view(), name = 'get_all_camera_of_current_isp'),
    path('update', CameraUpdateAPIView.as_view(), name = 'update_camera'),
    path('id/<int:pk>', CameraUpdateAPIView.as_view(), name = 'get_camera_by_id'),
    path('delete', CameraDeleteAPIView.as_view(), name = 'delete_camera'),
]
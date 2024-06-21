from django.urls import path
from .views import HeaderAPIView, HeaderDeleteAPIView

urlpatterns = [
    path('header', HeaderAPIView.as_view(), name='header_api'),
    path('header/add', HeaderAPIView.as_view(), name='header_add_api'),
    path('header/delete', HeaderDeleteAPIView.as_view(), name='delete-header'),
]
from django.urls import path
from .views import HeaderAPIView, HeaderDeleteAPIView, FooterAPIView, FooterDeleteAPIView, VideoAddAPIView

urlpatterns = [
    path('header', HeaderAPIView.as_view(), name='header_api'),
    path('header/add', HeaderAPIView.as_view(), name='header_add_api'),
    path('header/delete', HeaderDeleteAPIView.as_view(), name='delete-header'),
    path('footer', FooterAPIView.as_view(), name='footer_api'),
    path('footer/add', FooterAPIView.as_view(), name='footer_add_api'),
    path('footer/delete', FooterDeleteAPIView.as_view(), name='delete-footer'),
    path('video/add', VideoAddAPIView.as_view(), name='add-video'),
]
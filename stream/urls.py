from django.urls import path
from .views import start_stream, stop_stream_view

urlpatterns = [
    path('start_stream', start_stream, name='start_stream'),
    path('stop_stream', stop_stream_view, name='stop_stream'),
]

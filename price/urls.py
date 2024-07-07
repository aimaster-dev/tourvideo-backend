from django.urls import path
from .views import PriceAPIView, PriceDeleteAPIView, PriceGetAllAPIView, PriceUpdateAPIView

urlpatterns = [
    path('add', PriceAPIView.as_view(), name = 'price_add'),
    path('getall', PriceGetAllAPIView.as_view(), name = 'get_all_price_type'),
    path('update', PriceUpdateAPIView.as_view(), name = 'update_price'),
    path('delete', PriceDeleteAPIView.as_view(), name = 'delete_price'),
]
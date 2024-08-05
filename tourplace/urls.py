from django.urls import path
from .views import TourplaceAPIView, TourplaceUpdateAPIView, TourplaceDeleteAPIView, TourplaceGetAllAPIView, TourplaceGetAllForISPAPIView, TourplaceGetAllForCamAPIView

urlpatterns = [
    path('add', TourplaceAPIView.as_view(), name = 'tourplace_add'),
    path('get', TourplaceAPIView.as_view(), name = 'tourplace_get'),
    path('getall', TourplaceGetAllAPIView.as_view(), name = 'get_all_tourplace_type'),
    path('update', TourplaceUpdateAPIView.as_view(), name = 'update_tourplace'),
    path('delete', TourplaceDeleteAPIView.as_view(), name = 'delete_tourplace'),
    path('id/<int:pk>', TourplaceUpdateAPIView.as_view(), name='get-tourplace-by-id'),
    path('getispall', TourplaceGetAllForISPAPIView.as_view(), name='get-tourplace-for-isp'),
    path('gettourbyisp', TourplaceGetAllForCamAPIView.as_view(), name='get-tourplace-for-cam'),
]
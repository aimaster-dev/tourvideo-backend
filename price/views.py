from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.permissions import IsAdmin, IsISP
from .models import Price
from django.shortcuts import get_object_or_404
from .serializers import PriceSerializer
from rest_framework.response import Response
from rest_framework import status
from tourplace.models import TourPlace
# Create your views here.

class PriceAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        if user.usertype == 2:
            tourplace_id = request.data.get('tourplace')
            data = request.data
            data["tourplace"] = TourPlace.objects.get(id = tourplace_id).pk
            serializer = PriceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': False, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': False, 'data': {"msg": "You don't have any permission to creat price."}}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def get(self, request, pk, format=None):
        price = get_object_or_404(Price, pk=pk)
        serializer = PriceSerializer(price)
        return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    
class PriceUpdateAPIView(APIView):
    
    permission_classes = [IsISP]
    
    def post(self, request):
        id = request.data["id"]
        price = Price.objects.get(id = id)
        tourplace_id = request.data.get("tourplace")
        data = request.data
        data["tourplace"] = TourPlace.objects.get(id = tourplace_id).pk
        serializer = PriceSerializer(price, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PriceDeleteAPIView(APIView):
    
    permission_classes = [IsISP]

    def post(self, request):
        id = request.data.get('id')
        if not id:
            return Response({"status": False, "data": {"msg": "Price ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            price = Price.objects.get(id=id)
            price.delete()
            return Response({"status": True, "data": {"msg": "Successfully Deleted."}}, status=status.HTTP_200_OK)
        except price.DoesNotExist:
            return Response({"status": False, "data": {"msg": "Price not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

class PriceGetAllAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tourplace_id = request.query_params.get("tourplace")
        Prices = []
        if tourplace_id:
            tourplace = TourPlace.objects.get(id = tourplace_id)
            Prices = Price.objects.filter(tourplace = tourplace.pk)
        else:
            if user.usertype == 1:
                tourplace = TourPlace.objects.all().first()
                Prices = Price.objects.filter(tourplace = tourplace.pk)
            elif user.usertype == 2:
                tourplace = TourPlace.objects.filter(isp = user.pk).first()
                Prices = Price.objects.filter(tourplace = tourplace.pk)
            elif user.usertype == 3:
                tour_id = user.tourplace[0]
                tourplace = TourPlace.objects.get(id = tour_id)
                Prices = Price.objects.filter(tourplace = tourplace.pk)
        serializer = PriceSerializer(Prices, many = True)
        return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
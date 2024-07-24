from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from user.permissions import IsAdmin, IsAdminOrISP
from .models import Price
from django.shortcuts import get_object_or_404
from .serializers import PriceSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class PriceAPIView(APIView):
    
    permission_classes = [IsAdmin]
    
    def post(self, request):
        user = request.user
        if user.usertype == 1:
            data = request.data
            serializer = PriceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': False, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': False, 'data': {'msg': 'You do not any permission to create the Price.'}})
    
    def get(self, request, pk, format=None):
        price = get_object_or_404(Price, pk=pk)
        serializer = PriceSerializer(price)
        return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    
class PriceUpdateAPIView(APIView):
    
    permission_classes = [IsAdmin]
    
    def post(self, request):
        id = request.data["id"]
        place = Price.objects.get(id = id)
        data = request.data
        serializer = PriceSerializer(place, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'data': {'msg': 'You do not any permission to create the Price.'}})

class PriceDeleteAPIView(APIView):
    
    permission_classes = [IsAdmin]

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
    permission_classes = [AllowAny]

    def get(self, request):
        Prices = Price.objects.all()
        serializer = PriceSerializer(Prices, many = True)
        return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
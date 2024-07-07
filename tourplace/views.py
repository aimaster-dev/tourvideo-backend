from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAdmin, IsAdminOrISP
from models import TourPlace
from django.shortcuts import get_object_or_404
from serializers import TourplaceSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class TourplaceAPIView(APIView):
    
    permission_classes = [IsAdminOrISP]

    def get(self, request):
        user = request.user
        if user is not None and user.usertype == 2:
            tourplace = get_object_or_404(TourPlace, pk=user.tourplace)
            data = {
                'id': tourplace.id,
                'place_name': tourplace.place_name,
                'status': tourplace.status,
                'created_at': tourplace.created_at,
                'updated_at': tourplace.updated_at,
            }
            return Response({'status': True, 'data': data}, status=status.HTTP_200_OK)
        if user.usertype == 1:
            tourplaces = TourPlace.objects.all()
            serializer = TourplaceSerializer(tourplaces, many = True)
            return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'data': {'msg': 'You have to login.'}}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request):
        user = request.user
        if user.usertype == 1:
            data = request.data
            serializer = TourplaceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': False, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': False, 'data': {'msg': 'You do not any permission to create the tourplace.'}})
    
class TourplaceUpdateAPIView(APIView):
    
    permission_classes = [IsAdmin]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Camera
from .serializers import CameraSerializer
from user.permissions import IsISP
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.

class CameraAPIView(APIView):
    permission_classes = [IsISP]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        isp = request.user
        if isp.usertype == 1:
            cameras = Camera.objects.all()
            serializer = CameraSerializer(cameras, many=True)
            return Response({'status': True, 'data': serializer.data})
        elif isp is not None:
            cameras = Camera.objects.filter(isp=isp.pk)
            serializer = CameraSerializer(cameras, many=True)
            return Response({'status': True, 'data': serializer.data})
        else:
            return Response({'status': False, 'error': 'You have to login in this site.'}, status=400)
        
    def post(self, request):
        serializer = CameraSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(isp = request.user)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "data": {"msg": serializer.errors["non_field_errors"][0]}}, status=status.HTTP_400_BAD_REQUEST)
    
class CameraUpdateAPIView(APIView):
    permission_classes = [IsISP]
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, pk, format=None):
        isp = request.user
        camera_id = pk
        if isp is not None:
            camera = Camera.objects.get(isp=isp, id = camera_id)
            serializer = CameraSerializer(camera)
            return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'error': 'You have to login in this site.'}, status=400)

    def post(self, request):
        camera_id = request.data.get('id')
        try:
            camera = Camera.objects.get(id=camera_id, isp=request.user)
            data = request.data
            data = {
                "camera_name": data.get("camera_name"),
                "camera_ip": data.get("camera_ip"),
                "camera_port": data.get("camera_port"),
                "camera_user_name": data.get("camera_user_name"),
                "password": data.get("password")
            }
            serializer = CameraSerializer(camera, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"status": False, "data": {"msg": serializer.errors}})
        except Camera.DoesNotExist:
            try:
                camera_existence = Camera.objects.get(id = camera_id)
                return Response({"status": False, "data": {"msg": "You don't have permission to delete this camera."}}, status=status.HTTP_403_FORBIDDEN)
            except Camera.DoesNotExist:
                return Response({"status": False, "data": {"msg": "Camera not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
        
class CameraDeleteAPIView(APIView):
    permission_classes = [IsISP]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        camera_id = request.data.get('id')
        if not camera_id:
            return Response({"status": False, "data": {"msg": "Header ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            camera = Camera.objects.get(id=camera_id, isp=request.user)
            camera.delete()
            return Response({"status": True, "data": {"msg": "Successfully Deleted."}}, status=status.HTTP_200_OK)
        except Camera.DoesNotExist:
            try:
                camera_existence = Camera.objects.get(id = camera_id)
                return Response({"status": False, "data": {"msg": "You don't have permission to delete this camera."}}, status=status.HTTP_403_FORBIDDEN)
            except Camera.DoesNotExist:
                return Response({"status": False, "data": {"msg": "Camera not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
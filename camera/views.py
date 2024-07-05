from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Camera
from .serializers import CameraSerializer
from user.permissions import IsISP
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import convert_rtsp_to_hls, get_output_dir, stop_stream
import requests
import json
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
        data = request.data
        rtsp_url = "rtsp://" + data.get("camera_user_name") + ":" + data.get("password") + "@" + data.get("camera_ip") + ":" + data.get("camera_port") + "/"
        output_dir = get_output_dir(rtsp_url)
        data = {
            "camera_name": data.get("camera_name"),
            "camera_ip": data.get("camera_ip"),
            "camera_port": data.get("camera_port"),
            "camera_user_name": data.get("camera_user_name"),
            "password": data.get("password"),
            "output_url": output_dir
        }
        serializer = CameraSerializer(data = data)
        if serializer.is_valid():
            serializer.save(isp = request.user)
            convert_rtsp_to_hls(rtsp_url, output_dir)
            # hls_url = f'/{output_dir}/index.m3u8'
    # return JsonResponse({'hls_url': hls_url})
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
            origin_dir = camera.output_url
            if not origin_dir:
                return Response({'status': False, 'error': 'Origin Dir is not existed now.'}, status=400)
            
            origin_dir = origin_dir.lstrip('/')
            stop_stream(origin_dir)
            data = request.data
            rtsp_url = "rtsp://" + data.get("camera_user_name") + ":" + data.get("password") + "@" + data.get("camera_ip") + ":" + data.get("camera_port") + "/"
            output_dir = get_output_dir(rtsp_url)
            data = {
                "camera_name": data.get("camera_name"),
                "camera_ip": data.get("camera_ip"),
                "camera_port": data.get("camera_port"),
                "camera_user_name": data.get("camera_user_name"),
                "password": data.get("password"),
                "output_url": output_dir
            }
            serializer = CameraSerializer(camera, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                convert_rtsp_to_hls(rtsp_url, output_dir)
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
            output_url = camera.output_url
            if not output_url:
                return Response({'status': False, 'error': 'Origin Dir is not existed now.'}, status=400)
            
            output_url = output_url.lstrip('/')
            stop_stream(output_url)
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
        
class CameraCheckAPIView(APIView):
    def post(self, request):
        userdata = request.data
        ip_addr = userdata["camera_ip"]
        userName = userdata["userName"]
        password = userdata["password"]

        url = f'https://{ip_addr}/api.cgi?cmd=Login'
        headers = {
            'Content-Type': 'application/json'
        }
        data = [
            {
                "cmd": "Login",
                "param": {
                    "User": {
                        "Version": "0",
                        "userName": userName,
                        "password": password
                    }
                }
            }
        ]
        try:
            response = requests.get(url, headers=headers, data=json.dumps(data), verify=False)
            response.raise_for_status()
            
            # Parse the JSON response
            data = json.loads(response.text)
            print(data)
            print(data[0]["code"])
            return Response({"status": True, "data": "Connected"}, status=status.HTTP_200_OK)
        
        except requests.exceptions.HTTPError as http_err:
            return Response({"status": False, "data": f'HTTP error occurred: {http_err}', 'content': response.content.decode()}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError as conn_err:
            return Response({"status": False, "data": f'Connection error occurred: {conn_err}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except requests.exceptions.Timeout as timeout_err:
            return Response({"status": False, "data": f'Timeout error occurred: {timeout_err}'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException as req_err:
            return Response({"status": False, "data": f'Request error occurred: {req_err}'}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError as json_err:
            return Response({"status": False, "data": f'JSON decode error: {json_err}', 'content': response.text}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"status": False, "data": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Header, Footer, Video
from .serializers import HeaderSerializer, FooterSerializer, VideoSerializer
from user.permissions import IsAdmin
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
import subprocess
from django.conf import settings
import os
from tourplace.models import TourPlace
from django.http import Http404, FileResponse

class HeaderAPIView(APIView):
    permission_classes = [IsAdmin]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        if self.request.user.usertype == 1:
            header = Header.objects.first()
            if header and header.tourplace:
                tourplace = header.tourplace
                return Header.objects.filter(tourplace = tourplace.pk)
            else:
                return Header.objects.none()
        return Header.objects.filter(user=self.request.user)
    
    def get(self, request):
        tourplace_id = request.query_params.get('tourplace')
        if tourplace_id == None:
            headers = self.get_queryset()
            if headers.exists():
                serializer = HeaderSerializer(headers, many=True)
                return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": True, "data": []}, status=status.HTTP_200_OK)
        else:
            tourplace = TourPlace.objects.get(id = tourplace_id)
            headers = Header.objects.filter(tourplace = tourplace.pk)
            if headers.exists():
                    serializer = HeaderSerializer(headers, many=True)
                    return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": True, "data": []}, status=status.HTTP_200_OK)
    
    def post(self, request):
        tourplace_id = request.data.get('tourplace')
        data = request.data
        data['tourplace'] = TourPlace.objects.get(id = tourplace_id).pk
        serializer = HeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class HeaderDeleteAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdmin]
    def post(self, request, *args, **kwargs):
        header_id = request.data.get('header_id')
        if not header_id:
            return Response({"status": False, "data": {"msg": "Header ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            header = Header.objects.get(pk=header_id, user=request.user)
            if header.video_path:
                if default_storage.exists(header.video_path.name):
                    default_storage.delete(header.video_path.name)
            if header.thumbnail:
                if default_storage.exists(header.thumbnail.name):
                    default_storage.delete(header.thumbnail.name)
            header.delete()
            return Response({"status": True}, status=status.HTTP_200_OK)
        except Header.DoesNotExist:
            try:
                header_existence = Header.objects.get(pk = header_id)
                return Response({"status": False, "data": {"msg": "You don't have permission to delete this data."}}, status=status.HTTP_403_FORBIDDEN)
            except Header.DoesNotExist:
                return Response({"status": False, "data": {"msg": "Header not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

class FooterAPIView(APIView):
    permission_classes = [IsAdmin]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        if self.request.user.usertype == 1:
            footer = Footer.objects.first()
            if footer and footer.tourplace:
                tourplace = footer.tourplace
                return Footer.objects.filter(tourplace = tourplace.pk)
            else:
                return Footer.objects.none()
        return Footer.objects.filter(user=self.request.user)
    
    def get(self, request):
        tourplace_id = request.query_params.get('tourplace')
        if tourplace_id == None:
            footers = self.get_queryset()
            if footers.exists():
                serializer = FooterSerializer(footers, many=True)
                return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": True, "data": []}, status=status.HTTP_200_OK)
        else:
            # print(tourplace_id)
            tourplace = TourPlace.objects.get(id = tourplace_id)
            footers = Footer.objects.filter(tourplace = tourplace.pk)
            if footers.exists():
                serializer = FooterSerializer(footers, many=True)
                return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": True, "data": []}, status=status.HTTP_200_OK)
    
    def post(self, request):
        tourplace_id = request.data.get('tourplace')
        data = request.data
        data['tourplace'] = TourPlace.objects.get(id = tourplace_id).pk
        serializer = FooterSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class FooterDeleteAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdmin]
    def post(self, request, *args, **kwargs):
        footer_id = request.data.get('footer_id')
        if not footer_id:
            return Response({"status": False, "data": {"msg": "Footer ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            footer = Footer.objects.get(pk=footer_id, user=request.user)
            if footer.video_path:
                if default_storage.exists(footer.video_path.name):
                    default_storage.delete(footer.video_path.name)
            if footer.thumbnail:
                if default_storage.exists(footer.thumbnail.name):
                    default_storage.delete(footer.thumbnail.name)
            footer.delete()
            return Response({"status": True}, status=status.HTTP_200_OK)
        except Footer.DoesNotExist:
            try:
                footer_existence = Footer.objects.get(pk = footer_id)
                return Response({"status": False, "data": {"msg": "You don't have permission to delete this data."}}, status=status.HTTP_403_FORBIDDEN)
            except Footer.DoesNotExist:
                return Response({"status": False, "data": {"msg": "Footer not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

class VideoAddAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        tourplace_id = request.data.get('tourplace_id')
        if not tourplace_id:
            return Response({'error': 'Tourplace ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tourplace = TourPlace.objects.get(pk=tourplace_id)
        except TourPlace.DoesNotExist:
            return Response({'error': 'Invalid Tourplace ID'}, status=status.HTTP_400_BAD_REQUEST)
        if 'video_path' not in request.FILES:
            return Response({'error': 'Video file is required'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        data['client'] = request.user.pk
        data['tourplace'] = tourplace_id
        serializer = VideoSerializer(data=data)
        if serializer.is_valid():
            uploaded_video = request.FILES['video_path']
            original_filename = uploaded_video.name
            temp_video_path = os.path.join(settings.MEDIA_ROOT, f'temp_uploaded_video_{request.user.username}.webm')
            with open(temp_video_path, 'wb+') as temp_file:
                for chunk in uploaded_video.chunks():
                    temp_file.write(chunk)
            video = serializer.save(client=request.user, tourplace=tourplace, status=False)
            subprocess.Popen(
                ['D:\\Project\\MyProject\\OttisTourist\\1880_video_update_backend\\otisenv\\Scripts\\python.exe', 'D:\\Project\\MyProject\\OttisTourist\\1880_video_update_backend\\tourvideoproject\\videomgmt\\video_processing.py', str(video.id), str(request.user.id), original_filename]
            )
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user
        if user.usertype == 1:
            videos = Video.objects.all()
            serializer = VideoSerializer(videos, many = True)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        elif user.usertype == 2:
            videos = Video.objects.filter(tourplace__in = user.tourplace)
            serializer = VideoSerializer(videos, many = True)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        elif user.usertype == 3:
            videos = Video.objects.filter(client = user.pk)
            serializer = VideoSerializer(videos, many = True)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        
def download_video(request):
    video_url = request.GET.get('video_url')
    if not video_url:
        raise Http404("Video URL not provided")

    video_path = os.path.join(settings.MEDIA_ROOT, video_url.replace('http://localhost:8000/media/', '').replace('/', os.sep))
    if not os.path.exists(video_path):
        raise Http404("Video not found")

    response = FileResponse(open(video_path, 'rb'), as_attachment=True, filename=os.path.basename(video_path))
    return response
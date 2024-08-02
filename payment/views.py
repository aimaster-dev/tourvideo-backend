from user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.permissions import IsClient
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.
class HeaderAPIView(APIView):
    permission_classes = [IsClient]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        return Response({"status": False, "data": 0}, status=status.HTTP_400_BAD_REQUEST)
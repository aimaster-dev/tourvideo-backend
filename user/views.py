from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .serializers import UserRegUpdateSerializer, UserListSerializer, UserLoginSerializer, UserDetailSerializer
from .models import User
from .permissions import IsAdmin
# Create your views here.

class UserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegUpdateSerializer(data = request.data)
        print(serializer)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "data": "User Registered Successfully."}, status = status.HTTP_201_CREATED)
        return Response({"status": False, "data": "Email is already used now."}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk, format=None):
        print(pk)
        try:
            user = User.objects.get(id = pk)
            serializer = UserDetailSerializer(user)
            return Response({"status": True, "data": serializer.data})
        except user.DoesNotExist:
            Response({"status": False, "data": {"msg": "User not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
    
class UserDeleteAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"status": False, "data": {"msg": "User ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id = user_id)
            user.delete()
            return Response({"status": True, "data": "The User Successfully deleted."}, status=status.HTTP_200_OK)
        except user.DoesNotExist:
            Response({"status": False, "data": {"msg": "User not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid():
            if serializer.validated_data['status'] == False and serializer.validated_data['user_type'] == 2:
                return Response({"status": False, "data": {"msg": "Please wait until admin allows you"}}, status=status.HTTP_423_LOCKED)
            else:
                return Response({"status": True, "data": serializer.validated_data}, status=status.HTTP_200_OK)
        return Response({"status": False, "data": {"msg": "Invalid email or password"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
class UserUpdateAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        print(user_id)
        user = User.objects.get(id = user_id)
        print(user)
        if user == None:
            Response({"status": False, "data": "User isn't existed now."}, status=status.HTTP_404_NOT_FOUND)
        userdata = request.data
        serializer = UserRegUpdateSerializer(user, data=userdata, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class UserRangeListAPIView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]  # Assuming you want this endpoint to be protected

    def get_queryset(self):
        """
        Optionally restricts the returned users to a given range,
        by filtering against a `start_row_index` and `end_row_index` query parameter in the URL.
        """
        queryset = User.objects.all()
        start_row_index = self.request.query_params.get('start_row_index', None)
        end_row_index = self.request.query_params.get('end_row_index', None)

        if start_row_index is not None and end_row_index is not None:
            start_row_index = int(start_row_index)
            end_row_index = int(end_row_index)
            return queryset[start_row_index:end_row_index]
        return queryset
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .serializers import UserRegUpdateSerializer, UserListSerializer, UserLoginSerializer, UserDetailSerializer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import User, Invitation
from .permissions import IsAdmin, IsAdminOrISP
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from tourplace.models import TourPlace
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.db.models import F, Func
# Create your views here.

def is_subset(small, big):
    return all(item in big for item in small)

class UserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegUpdateSerializer(data = request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            user = serializer.save()
            serializer.is_active = False
            user.save()
            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_url = f"https://emmysvideos.com/email_verify?uid={uid}&token={token}"
            mail_subject = 'Activate your account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'activation_url': activation_url,
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = "html"
            email.send()
            return Response({"status": True, "data": "User Registered Successfully. Please check your email to activate your account."}, status = status.HTTP_201_CREATED)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(id = pk)
            serializer = UserDetailSerializer(user)
            data = serializer.data
            tourpl = data['tourplace']
            del data['tourplace']
            data['tourplace'] = []
            for tour in tourpl:
                tour_data = {
                    'id': tour,
                    'place_name': TourPlace.objects.get(id = tour).place_name
                }
                data['tourplace'].append(tour_data)
            return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
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
            tourplace = user.tourplace
            for tour in tourplace:
                print(tour)
            user.delete()
            return Response({"status": True, "data": "The User Successfully deleted."}, status=status.HTTP_200_OK)
        except user.DoesNotExist:
            Response({"status": False, "data": {"msg": "User not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        tourplace = request.data.get("tourplace")
        print(tourplace)
        login_data = request.data
        login_data.pop("tourplace", None)
        serializer = UserLoginSerializer(data = login_data)
        if serializer.is_valid():
            validated_data =serializer.validated_data
            if validated_data['status'] == False and validated_data['usertype'] == 2:
                return Response({"status": False, "data": {"msg": "Please wait until admin allows you"}}, status=status.HTTP_423_LOCKED)
            else:
                user = validated_data.pop('user')
                user.tourplace = tourplace
                user.save()
                return Response({"status": True, "data": serializer.validated_data}, status=status.HTTP_200_OK)
        return Response({"status": False, "data": {"msg": "Invalid email or password"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
class UserUpdateAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        user = User.objects.get(id = user_id)
        print(user)
        if user == None:
            Response({"status": False, "data": "User isn't existed now."}, status=status.HTTP_404_NOT_FOUND)
        origin_tour = user.tourplace
        for tour in origin_tour:
            place = TourPlace.objects.get(id = tour)
            place.isp = 0
            place.save()
        userdata = request.data
        serializer = UserRegUpdateSerializer(user, data=userdata, partial = True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            tourplaces = data['tourplace']
            del data['tourplace']
            data['tourplace'] = []
            for tourplace in tourplaces:
                tour_data = {
                    'id': tourplace,
                    'place_name': TourPlace.objects.get(id = tourplace).place_name
                }
                data['tourplace'].append(tour_data)
                if user.usertype == 2:
                    place = TourPlace.objects.get(id = tourplace)
                    place.isp = user.pk
                    place.save()
            return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class ISPRangeListAPIView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]  # Assuming you want this endpoint to be protected

    def get_queryset(self):
        """
        Optionally restricts the returned users to a given range,
        by filtering against a `start_row_index` and `end_row_index` query parameter in the URL.
        """
        queryset = User.objects.filter(usertype = 2)
        start_row_index = self.request.query_params.get('start_row_index', None)
        end_row_index = self.request.query_params.get('end_row_index', None)

        if start_row_index is not None and end_row_index is not None:
            start_row_index = int(start_row_index)
            end_row_index = int(end_row_index)
            return queryset[start_row_index:end_row_index]
        return queryset
    
class ClientRangeListAPIView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdminOrISP]  # Assuming you want this endpoint to be protected
    def get_queryset(self):
        """
        Optionally restricts the returned users to a given range,
        by filtering against a `start_row_index` and `end_row_index` query parameter in the URL.
        """
        queryset = []
        a = self.request.user.tourplace if self.request.user.usertype == 2 else []
        if self.request.user.usertype == 1:
            queryset = User.objects.filter(usertype = 3)
        elif self.request.user.usertype == 2:
            all_users = User.objects.filter(usertype=3)
            for user in all_users:
                if is_subset(user.tourplace, a):
                    queryset.append(user)
        start_row_index = self.request.query_params.get('start_row_index', None)
        end_row_index = self.request.query_params.get('end_row_index', None)

        if start_row_index is not None and end_row_index is not None:
            start_row_index = int(start_row_index)
            end_row_index = int(end_row_index)
            return queryset[start_row_index:end_row_index]
        return queryset
    
class ActivateAccount(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get("user_id")
        token = request.data.get("token")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            mail_subject = 'Activate Successfully'
            message = render_to_string('verification_success_email.html', {
                'user': user,
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = "html"
            email.send()
            return Response({"status": True, "data": "Your account has been successfully activated."}, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "data": "Activation link is invalid!"}, status=status.HTTP_400_BAD_REQUEST)


class ResendActivationEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                mail_subject = 'Activate your account.'
                token = account_activation_token.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                activation_url = f"https://emmysvideos.com/email_verify?uid={uid}&token={token}"
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'activation_url': activation_url,
                })
                email = EmailMessage(mail_subject, message, to=[user.email])
                email.content_subtype = "html"
                email.send()
                return Response({"status": True, "data": "A new activation email has been sent."}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, "data": "This account is already active."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"status": False, "data": "No user found with this email address."}, status=status.HTTP_404_NOT_FOUND)

class InviteUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        tourplace = request.data.get('tourplace')
        token = get_random_string(50)
        if request.user.usertype != 1:
            return Response({"status": True, "data": {"msg": "You don't have any permission to create ISP account."}})
        invited_by = request.user
        Invitation.objects.create(email = email, tourplace = tourplace, token = token, invited_by = invited_by)
        invitation_link = f"{request.scheme}://{request.get_host()}/set_password/{token}"
        subject = 'Invitation to Join'
        message = render_to_string('isp_register.html', {
            'invitation_link': invitation_link
        })
        email = EmailMessage(subject, message, to=[email])
        email.content_subtype = "html"
        email.send()
        return Response({"status": True, "data": {"msg": "Invitation Sent."}}, status=status.HTTP_200_OK)
    
class SetPasswordView(APIView):
    def post(self, request, token):
        invitation = get_object_or_404(Invitation, token = token)
        userdata = request.data
        userdata["tourplace"] = invitation.tourplace
        userdata["email"] = invitation.email
        userdata["usertype"] = 2
        serializer = UserRegUpdateSerializer(data = userdata)
        if serializer.is_valid():
            user = serializer.save()
            tourplaces = invitation.tourplace
            for tourplace in tourplaces:
                tourplace_model = TourPlace.objects.get(pk = tourplace)
                tourplace_model.isp = user.pk
                tourplace_model.save()
            user.is_invited = True
            user.status = True
            user.is_active = True
            user.save()
            invitation.delete()
            subject = 'Invitation to Join'
            message = render_to_string('isp_register_successfully.html')
            email = EmailMessage(subject, message, to=[userdata["email"]])
            email.content_subtype = "html"
            email.send()
            user_serializer = UserDetailSerializer(user)
            data = user_serializer.data
            del data['tourplace']
            data['tourplace'] = []
            for tourplace in tourplaces:
                tourdata = {
                    'id': tourplace,
                    'place_name': TourPlace.objects.get(id = tourplace).place_name
                }
                data['tourplace'].append(tourdata)
            return Response({"status": True, "data": data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
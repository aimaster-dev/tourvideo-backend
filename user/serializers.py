import datetime
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils import timezone
from rest_framework import serializers

class UserRegUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone_number', 'usertype', 'street', 'country', 'city', 'zipcode', 'state', 'get_same_video', 'status', 'appears_in_others_video', 'voice_can_be_recorded', 'be_shown_potential', 'be_shown_public_business', 'be_shown_social_media')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        print(user)
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.usertype = validated_data.get('usertype', instance.usertype)
        instance.street = validated_data.get('street', instance.street)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.zipcode = validated_data.get('zipcode', instance.zipcode)
        instance.state = validated_data.get('state', instance.state)
        instance.get_same_video = validated_data.get('get_same_video', instance.get_same_video)
        instance.appears_in_others_video = validated_data.get('appears_in_others_video', instance.appears_in_others_video)
        instance.voice_can_be_recorded = validated_data.get('voice_can_be_recorded', instance.voice_can_be_recorded)
        instance.be_shown_potential = validated_data.get('be_shown_potential', instance.be_shown_potential)
        instance.be_shown_public_business = validated_data.get('be_shown_public_business', instance.be_shown_public_business)
        instance.be_shown_social_media = validated_data.get('be_shown_social_media', instance.be_shown_social_media)
        instance.save()
        return super().update(instance, validated_data)

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'usertype', 'street', 'country', 'city', 'zipcode', 'state', 'get_same_video', 'appears_in_others_video', 'voice_can_be_recorded', 'be_shown_potential', 'be_shown_public_business', 'be_shown_social_media']  # Exclude 'password'
        read_only_fields = fields

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        # print(data['email'])
        # print(data['password'])
        user = authenticate(email=data['email'], password=data['password'])
        # print(user)
        if user and user.created_at + datetime.timedelta(hours=4) > timezone.now():
        # if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return {
                'refresh': str(refresh),
                'access': str(access),
                'user_id': user.id,
                'usertype': user.usertype,
                'username': user.username,
                'status' : user.status,
            }
        else:
            raise serializers.ValidationError("Invalid email or password")
        
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)  # Exclude password from the serialized data
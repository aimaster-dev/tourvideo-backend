from rest_framework import serializers
from .models import Camera
from tourplace.models import TourPlace
from tourplace.serializers import TourplaceSerializer

class CameraSerializer(serializers.ModelSerializer):
    # tourplace = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = ['id', 'camera_name', 'camera_ip', 'camera_port', 'camera_user_name', 'password', 'output_url', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        if self.instance:
            return attrs
        camera_ip = attrs.get('camera_ip')
        camera_port = attrs.get('camera_port')
        if Camera.objects.filter(camera_ip=camera_ip, camera_port=camera_port).exists():
            raise serializers.ValidationError("A camera with this IP address and port already exists.")
        return super().validate(attrs)
    
    # def get_tourplace(self, obj):
    #     tourplace_ids = obj.tourplace  # This assumes `obj.tourplace` is a list of IDs
    #     print(tourplace_ids)
    #     tourplaces = TourPlace.objects.filter(id__in=tourplace_ids)
    #     return TourplaceSerializer(tourplaces, many=True).data

class CameraUpdateSerializer(serializers.ModelSerializer):
    tourplace = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = ['id', 'camera_name', 'camera_ip', 'camera_port', 'camera_user_name', 'password', 'output_url', 'tourplace', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        if self.instance:
            return attrs
        camera_ip = attrs.get('camera_ip')
        camera_port = attrs.get('camera_port')
        if Camera.objects.filter(camera_ip=camera_ip, camera_port=camera_port).exists():
            raise serializers.ValidationError("A camera with this IP address and port already exists.")
        return super().validate(attrs)
    
    def get_tourplace(self, obj):
        tourplace = obj.tourplace  # This assumes `obj.tourplace` is a list of IDs
        print(tourplace)
        tourplaces = TourPlace.objects.filter(id=tourplace.pk)
        return TourplaceSerializer(tourplaces, many=True).data
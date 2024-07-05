from rest_framework import serializers
from .models import Camera

class CameraSerializer(serializers.ModelSerializer):

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
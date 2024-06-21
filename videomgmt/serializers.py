from rest_framework import serializers
from .models import Header

class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = ['id', 'video_path', 'created_at', 'updated_at', 'thumbnail']
        read_only_fields = ['thumbnail']  # Make 'thumbnail' field read-only

    def create(self, validated_data):
        # Create a new Header instance using the validated data.
        header_instance = Header.objects.create(**validated_data)
        return header_instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
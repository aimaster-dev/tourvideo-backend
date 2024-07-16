from rest_framework import serializers
from .models import TourPlace

class TourplaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TourPlace
        fields = ["id", "place_name", "status", "isp", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        # print(validated_data)
        instance.place_name = validated_data.get('place_name', instance.place_name)
        instance.status = validated_data.get('status', instance.status)
        instance.isp = validated_data.get('isp', instance.isp)
        instance.save()
        return instance
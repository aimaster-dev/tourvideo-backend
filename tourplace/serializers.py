from rest_framework import serializers
from .models import TourPlace

class TourplaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TourPlace
        fields = ["place_name", "status", "created_at", "updated_at"]
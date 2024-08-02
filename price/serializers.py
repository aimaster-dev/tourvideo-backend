from rest_framework import serializers
from .models import Price

class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ["id", "price", "level", "title", "tourplace", "record_time", "record_limit", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
from rest_framework import serializers
from .models import Price

class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ["id", "price", "level", "title", "record_time", "record_limit", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.level = validated_data.get('level', instance.level)
        instance.title = validated_data.get('title', instance.title)
        instance.record_time = validated_data.get('record_time', instance.record_time)
        instance.record_limit = validated_data.get('record_limit', instance.record_limit)
        instance.save()
        return instance
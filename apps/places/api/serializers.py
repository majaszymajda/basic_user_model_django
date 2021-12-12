from rest_framework import serializers

from apps.places.models import City, Workstation


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "url", "city", "is_active")
        extra_kwargs = {"id": {"read_only": True}}


class WorkstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workstation
        fields = ("id", "url", "workstation", "is_active")
        extra_kwargs = {"id": {"read_only": True}}

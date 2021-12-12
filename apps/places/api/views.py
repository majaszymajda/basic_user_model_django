from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from apps.places.api.serializers import CitySerializer, WorkstationSerializer
from apps.places.models import City, Workstation


class CityView(
    CreateModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = (
        "city",
        "is_active",
    )


class WorkstationView(
    CreateModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Workstation.objects.all()
    serializer_class = WorkstationSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ("workstations", "is_active")

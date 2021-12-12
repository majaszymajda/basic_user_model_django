from django.urls import include, path

from rest_framework import routers

from apps.places.api.views import CityView, WorkstationView

router = routers.DefaultRouter()
router.register("cities", CityView)
router.register("workstations", WorkstationView)

urlpatterns = [path("", include(router.urls))]

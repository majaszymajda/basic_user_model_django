from django.urls import include, path

from rest_framework import routers

from apps.users.api.views import ProfileViewSet, UserViewSet

router = routers.DefaultRouter()

router.register("profiles", ProfileViewSet)
router.register("users", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

from django.conf.urls import url
from django.urls import include, path

from knox import views as knox_views

from apps.places.api import urls as places_urls
from apps.shifts.api import urls as shifts_urls
from apps.users.api import urls as user_urls
from apps.users.api.views import LoginAPIView, RegisterAPIView

urlpatterns = [
    path("places/", include(places_urls)),
    path("shifts/", include(shifts_urls)),
    path("users/", include(user_urls)),
    url("^auth/register/$", RegisterAPIView.as_view(), name="knox_register"),
    url("^auth/login/$", LoginAPIView.as_view(), name="knox_login"),
    url("^auth/logout/$", knox_views.LogoutView.as_view(), name="knox_logout"),
]

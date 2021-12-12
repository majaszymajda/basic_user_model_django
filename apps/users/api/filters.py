import django_filters
from django_filters import FilterSet

from apps.users.models import Profile


class UserFilters(FilterSet):

    last_name = django_filters.CharFilter(
        field_name="user__last_name", lookup_expr="icontains"
    )
    first_name = django_filters.CharFilter(
        field_name="user__first_name", lookup_expr="icontains"
    )
    username = django_filters.CharFilter(
        field_name="user__username", lookup_expr="icontains"
    )
    email = django_filters.CharFilter(field_name="user__email", lookup_expr="icontains")
    is_active = django_filters.BooleanFilter(field_name="user__is_active")
    workstation = django_filters.CharFilter(
        field_name="workstations__workstation", lookup_expr="icontains"
    )
    city = django_filters.CharFilter(
        field_name="work_city__city", lookup_expr="icontains"
    )

    class Meta:
        model = Profile

        fields = [
            "last_name",
            "first_name",
            "username",
            "email",
            "is_active",
            "workstation",
            "city",
        ]

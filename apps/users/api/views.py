from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.users.api.filters import UserFilters
from apps.users.api.pagination import PostLimitOffsetPagination
from apps.users.api.permissions import IsOwner, IsOwnerOrIsAdminOrReadOnly
from apps.users.api.serializers import (
    ForgotPasswordSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserPasswordUpdateSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from apps.users.models import Profile, User
from apps.utils.mixins import ActionPermissionMixin, ActionSerializerMixin


class ProfileViewSet(ActionSerializerMixin, ModelViewSet):

    action_serializers = {
        "partial_update": ProfileUpdateSerializer,
        "update": ProfileUpdateSerializer,
    }
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = PostLimitOffsetPagination
    permission_classes = [IsAuthenticated, IsOwnerOrIsAdminOrReadOnly]
    filterset_class = UserFilters
    ordering_fields = [
        "user__username",
        "user__email",
    ]
    ordering = ["user__username", "user__email"]
    search_fields = ["user__username", "user__email"]

    def perform_destroy(self, instance):
        instance.user.delete(soft=True)
        instance.delete(soft=True)


class UserViewSet(
    ActionSerializerMixin,
    ActionPermissionMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    action_serializers = {
        "update_password": UserPasswordUpdateSerializer,
        "update": UserUpdateSerializer,
        "create": ForgotPasswordSerializer,
    }

    action_permissions = {
        "update": [IsAdminUser],
        "create": [AllowAny],
    }

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PostLimitOffsetPagination

    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=["PUT"],
        name="password-update",
        url_path="password",
        permission_classes=[IsOwner],
    )
    def update_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            data={"message": "Hasło zostało zmienione"}, status=status.HTTP_200_OK
        )


class RegisterAPIView(CreateAPIView):

    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class LoginAPIView(CreateAPIView):

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            token = serializer.create(user)

            return Response(
                {
                    "profile": ProfileSerializer(
                        user.profile, context=self.get_serializer_context()
                    ).data,
                    "token": token,
                }
            )
        except BaseException:
            return Response(
                data={"message": "Logowanie zakończyło się niepowodzeniem."},
                status=status.HTTP_400_BAD_REQUEST,
            )

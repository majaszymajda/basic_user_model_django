from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from apps.users.models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "url",
            "is_removed",
            "is_active",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        password = BaseUserManager().make_random_password()
        user.set_password(password)

        user.save()
        send_mail(
            subject="Your password",
            message=password,
            from_email="",
            recipient_list=[f"{user.email}"],
            fail_silently=False,
        )
        return user


class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.CharField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():

            raise serializers.ValidationError(
                {"forgot_password": _("Podany email nie istnieje.")}
            )
        return value

    def create(self, validated_data, *args, **kwargs):
        user = User.objects.get(email=validated_data["email"])
        password = BaseUserManager().make_random_password()
        user.set_password(password)
        user.save()
        send_mail(
            subject="Your password",
            message=password,
            from_email="",
            recipient_list=[f"{user.email}"],
            fail_silently=False,
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("is_active", "first_name", "last_name")


class UserPasswordUpdateSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    default_error_messages = {"invalid_password": _("Nieprawidłowe hasło.")}

    def validate_old_password(self, value):
        user = self.context.get("view").get_object()
        if not user.check_password(value):
            self.fail("invalid_password")
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": _("Podane hasła nie są zgodne.")}
            )
        password_validation.validate_password(
            data["new_password"], self.context["request"].user
        )
        return data

    def update(self, instance, validated_data):

        instance.update_password(validated_data["new_password"])
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(
            _("Unable to log in with provided credentials.")
        )

    def create(self, instance):
        token = instance.create_token()
        return token


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    workstations = serializers.StringRelatedField(many=True)
    work_city = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "is_admin",
            "is_leader",
            "work_city",
            "workstations",
            "modification_time",
            "is_removed",
            "user",
        )
        extra_kwargs = {
            "workstations": {"required": False},
            "user": {"required": False, "read_only": True},
        }


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "work_city",
            "workstations",
        )

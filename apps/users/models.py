from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models

from knox.models import AuthToken

from apps.places.models import City, Workstation
from apps.utils.models import BaseModel


class User(AbstractUser, BaseModel):

    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def update_password(self, new_password):
        self.set_password(new_password)
        AuthToken.objects.filter(user_id=self.id).delete()

    def create_token(self):
        _, token = AuthToken.objects.create(user=self, expiry=timedelta(minutes=30))
        return token


class Profile(BaseModel):
    is_admin = models.BooleanField(default=True)
    is_leader = models.BooleanField(default=True)
    work_city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    workstations = models.ManyToManyField(Workstation, related_name="workstations")
    modification_time = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

from django.db import models
from django.utils.translation import gettext as _

from apps.utils.models import BaseModel


class City(BaseModel):
    class CityName(models.TextChoices):
        WROCLAW = _("Wrocław")
        RZESZOW = _("Rzeszów")
        INNE = _("Inne")

    city = models.CharField(
        max_length=20, choices=CityName.choices, default=CityName.WROCLAW
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.city


class Workstation(BaseModel):
    class WorkstationName(models.TextChoices):
        UX = _("UX Designer")
        UI = _("UI Designer")
        FRONTEND = _("Frontend")
        BACKEND = _("Backend")
        PHP = _("PHP")
        PYTHON = _("Python")
        REACT = _("React")
        MOBILE = _("Mobile")
        SCRUM_MASTER = _("Scrum Master")
        VUE = _("Vue")

    workstation = models.CharField(
        max_length=20, choices=WorkstationName.choices, default=WorkstationName.UX
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.workstation

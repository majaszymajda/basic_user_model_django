from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "apps.users"
    label = "core_users"

    def ready(self):
        __import__("apps.users.signals")

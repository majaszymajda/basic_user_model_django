class ActionSerializerMixin:
    """
    Mixin umożliwia wybór serializera w zależności od akcji i metody HTTP.
    Przykład użycia:
    action_serializers = {
        'list': ExampleListSerializer,
        'post': ExamplePostSerializer,
        'custom_action': CustomActionSerializer,
        'custom_action_get': CustomActionGetSerializer,
    }
    """

    action_serializers = {}

    def get_serializer_class(self):
        request_method_name = self.request.method.lower()
        if hasattr(self, "action"):
            action_method = f"{self.action}_{request_method_name}"
            # Kolejność wyboru:
            # 1. Na podstawie nazwy akcji i metody HTTP - action_method.
            # 2. Na podstawie nazwy akcji.
            # 3. Pierwotny serializer.

            return self.action_serializers.get(
                action_method,
                self.action_serializers.get(self.action, self.serializer_class),
            )
        # Dla widoków, które bazują na metodach HTTP a nie akcjach.

        return self.action_serializers.get(request_method_name, self.serializer_class)


class ActionPermissionMixin:
    """
    Mixin umożliwia wybór grupy uprawnień w zależności od akcji i metody HTTP.
    Przykład użycia:
    action_permissions = {
        'list': [AllowAny],
        'post': [IsAuthenticated],
        'custom_action': [IsAuthenticatedOrReadOnly],
        'custom_action_get': [CustomPermission],
    }
    """

    action_permissions = {}

    def get_permissions(self):
        request_method_name = self.request.method.lower()
        if hasattr(self, "action"):
            action_method = f"{self.action}_{request_method_name}"
            # Kolejność wyboru:
            # 1. Na podstawie nazwy akcji i metody HTTP - action_method.
            # 2. Na podstawie nazwy akcji.
            # 3. Pierwotne uprawnienia.
            return [
                permission()
                for permission in self.action_permissions.get(
                    action_method,
                    self.action_permissions.get(self.action, self.permission_classes),
                )
            ]
        # Dla widoków, które bazują na metodach HTTP a nie akcjach.
        return [
            permission()
            for permission in self.action_permissions.get(
                request_method_name, self.permission_classes
            )
        ]

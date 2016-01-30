from rest_framework.routers import DefaultRouter


class GSWDefaultRouter(DefaultRouter):

    def register(self, prefix, viewset, base_name=None):
        if base_name is None:
            base_name = prefix
        self.registry.append((prefix, viewset, base_name))
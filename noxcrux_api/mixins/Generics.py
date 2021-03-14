from rest_framework.generics import GenericAPIView
from rest_framework import mixins


class ListCreateDestroyAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    """
    Concrete view for listing a queryset, creating or deleting a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ListUpdateDestroyAPIView(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    """
    Concrete view for listing a queryset, updating or deleting a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

from rest_framework import mixins, viewsets, filters, status
from rest_framework.response import Response

from .permissions import (IsSuperUserOrReadOnly)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet,):
    permission_classes = (IsSuperUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

from collections import OrderedDict

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .serializers import UserSerializer, UserStatSerializer
from .models import User


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 366

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class UserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class UserStat(generics.ListAPIView):
    serializer_class = UserStatSerializer
    permission_classes = []
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        user = get_object_or_404(User, **filter_kwargs)

        return user.stat_set.all()

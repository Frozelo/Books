import django.db.models
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet, GenericViewSet

from orders.models import Books, UserBookRelation
from orders.serializers import BookSerializer, UserBookRelationSerializer, UserSerializer
from .logic_filter import BookFilter
from .permissions import IsOwnerOrReadOnly


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().annotate(annotated_likes_user=Count(Case(When(userbookrelation__like=True, then=1))))
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]


class BookViewSet(ModelViewSet):
    queryset = Books.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                            ).select_related(
        'owner').prefetch_related('readers').order_by('rating')
    # select related - вытягиваем владельца (когда работаем с ForeignKey - один ко многим)
    # prefetch related - вытягиваем читателей (когда работаем с ManyToMany - многие ко многим)

    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = BookFilter
    search_fields = ['author', 'name']
    ordering_fields = ['price', 'author', "annotated_likes"]

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        serializer.save()


class UserBookRelationViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book=self.kwargs['book'])
        return obj


def index_1(request):
    return render(request, 'index.html')


def auth(request):
    return render(request, 'oauth.html')

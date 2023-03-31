from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from orders.models import Books, UserBookRelation


class UserSerializer(ModelSerializer):
    annotated_likes_user = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', "username", "first_name", "last_name", 'annotated_likes_user')


class BookReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BookSerializer(ModelSerializer):
    # likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(
        read_only=True)  # read_only=True так как при запросе в IntegerField будут требоваться необходимые аргументы,
    # нам они не нужны!
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(source="owner.username",
                                       read_only=True)  # Так как при обычном обращении owner будет выдаваться число
    readers = BookReaderSerializer(many=True,
                                   read_only=True)  # many=True используется для того, чтобы отображались все user's

    class Meta:
        model = Books
        fields = ("id", "name", "price", "author", "owner_name", "readers", "annotated_likes", "rating")

    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ['book', 'like', 'rate', 'in_bookmarks']

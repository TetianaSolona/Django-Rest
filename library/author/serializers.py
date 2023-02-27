from rest_framework import serializers
from book.serializers import BookSerializer
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'surname', 'patronymic', 'books')

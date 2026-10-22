from rest_framework import serializers
from .models import Genre, Book, Comment

class BookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'published_year', 'description']

class GenreSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True, read_only=True)
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = '__all__'

    def get_books_count(self, obj):
        return obj.books.count()

class GenreDetailSerializer(serializers.ModelSerializer):
    books = BookInfoSerializer(many=True, read_only=True)
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = '__all__'

    def get_books_count(self, obj):
        return obj.books.count()

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            "price": {"min_value": 0},
            "published_year": {"min_value": 0, "max_value": 2100},
            "description": {"required": False},
            "genre": {"required": True, "allow_null": False}
        }

class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['created_at', 'user']

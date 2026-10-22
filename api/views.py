from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions,
)
from .models import Genre, Book, Comment
from .serializers import (
    GenreSerializer,
    GenreDetailSerializer,
    BookSerializer,
    BookDetailSerializer,
    CommentSerializer,
)
from .permissions import IsOwnerOrReadOnly
from .pagination import GenrePagination, BookPagination, CommentPagination


class GenreViewSet(ModelViewSet):
    """
    Janrlar bilan ishlash uchun API:
    - list: Janrlar ro'yxatini ko'rish
    - retrieve: Bitta janrni kitoblari bilan ko'rish
    - create: Yangi janr yaratish (admin/moderator)
    - update / destroy: Janrni tahrirlash va o'chirish
    """
    queryset = Genre.objects.all().prefetch_related('books').order_by('id')
    serializer_class = GenreSerializer
    permission_classes = [DjangoModelPermissions]
    pagination_class = GenrePagination

    def get_queryset(self):
        queryset = Genre.objects.all().prefetch_related('books').order_by('id')
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GenreDetailSerializer
        return GenreSerializer


class BookViewSet(ModelViewSet):
    """
    Kitoblar bilan ishlash uchun API:
    - list: Kitoblar ro'yxati (search, genre filter, pagination bilan)
    - retrieve: Bitta kitobni batafsil ko'rish
    - create: Yangi kitob qo'shish (add_book huquqi bilan)
    - update / partial_update: Kitobni tahrirlash (faqat admin)
    - destroy: Kitobni o'chirish (faqat admin)
    """
    queryset = Book.objects.all().select_related('genre').order_by('id')
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        queryset = Book.objects.all().select_related('genre').order_by('id')
        genre_id = self.request.query_params.get("genre")
        search = self.request.query_params.get("search")

        if genre_id and genre_id.isdigit():
            queryset = queryset.filter(genre_id=genre_id)

        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        if self.action == "create":
            return [DjangoModelPermissions()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return BookDetailSerializer
        return BookSerializer


class CommentViewSet(ModelViewSet):
    """
    Izohlar bilan ishlash uchun API:
    - list: Izohlarni ko'rish
    - create: Izoh qoldirish (faqat login qilganlar)
    - update / destroy: Faqat izoh egasi tahrirlaydi yoki o'chiradi
    """
    queryset = Comment.objects.all().select_related('user', 'book').order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = CommentPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

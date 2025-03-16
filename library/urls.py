from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet, MemberViewSet, BorrowRecordViewSet, borrow_book, return_book

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'members', MemberViewSet)
router.register(r'borrowrecords', BorrowRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('borrow/', borrow_book, name='borrow_book'),
    path('return/', return_book, name='return_book'),
]

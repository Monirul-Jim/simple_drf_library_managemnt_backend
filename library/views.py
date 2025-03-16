from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Author, Member, BorrowRecord
from .serializers import BookSerializer, AuthorSerializer, MemberSerializer, BorrowRecordSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer


@api_view(['POST'])
def borrow_book(request):
    serializer = BorrowRecordSerializer(data=request.data)
    if serializer.is_valid():
        book_id = request.data.get('book')
        try:
            book = Book.objects.get(pk=book_id)
            if not book.availability_status:
                return Response({'error': 'Book is not available for borrowing.'}, status=status.HTTP_400_BAD_REQUEST)
            book.availability_status = False
            book.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def return_book(request):
    book_id = request.data.get('book')
    member_id = request.data.get('member')

    try:
        borrow_record = BorrowRecord.objects.filter(
            book_id=book_id, member_id=member_id, return_date__isnull=True).latest('borrow_date')
        borrow_record.return_date = request.data.get('return_date')
        borrow_record.save()

        book = Book.objects.get(pk=book_id)
        book.availability_status = True
        book.save()

        return Response({'message': 'Book returned successfully.'}, status=status.HTTP_200_OK)

    except BorrowRecord.DoesNotExist:
        return Response({'error': 'Borrow record not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

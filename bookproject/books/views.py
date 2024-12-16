from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Book model
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom create method with additional error handling
        """
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            return Response({
                'error': 'Validation Failed',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def available_books(self, request):
        """
        Custom action to retrieve only available books
        """
        available_books = Book.objects.filter(is_available=True)
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'])
    def toggle_availability(self, request, pk=None):
        """
        Custom action to toggle book availability
        """
        book = self.get_object()
        book.is_available = not book.is_available
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method with soft delete option
        """
        instance = self.get_object()
        
        # Option to soft delete (mark as unavailable instead of removing)
        soft_delete = request.query_params.get('soft', 'false').lower() == 'true'
        
        if soft_delete:
            instance.is_available = False
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        # Default hard delete
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
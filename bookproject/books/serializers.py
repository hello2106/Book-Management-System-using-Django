from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model to handle validation and representation
    """
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_isbn(self, value):
        """
        Custom ISBN validation
        Checks if ISBN is unique and follows basic format
        """
        # Basic ISBN validation (can be expanded)
        if not (len(value) in [10, 13]):
            raise serializers.ValidationError("ISBN must be 10 or 13 characters long")
        
        # Check for uniqueness (excluding current instance during update)
        existing_books = Book.objects.filter(isbn=value)
        if self.instance:
            existing_books = existing_books.exclude(pk=self.instance.pk)
        
        if existing_books.exists():
            raise serializers.ValidationError("A book with this ISBN already exists")
        
        return value

    def validate_publication_year(self, value):
        """
        Validate publication year is not in the future
        """
        import datetime
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future")
        return value
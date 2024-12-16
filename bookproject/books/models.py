from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    """
    Model representing a book in the management system
    
    Fields:
    - title: The name of the book (required)
    - author: The author of the book (required)
    - isbn: International Standard Book Number (unique)
    - publication_year: Year the book was published
    - genre: Category of the book
    - total_pages: Number of pages in the book
    - rating: Book rating from 1 to 5
    - is_available: Availability status of the book
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000, "Publication year must be after 1000"),
            MaxValueValidator(2024, "Publication year cannot be in the future")
        ]
    )
    genre = models.CharField(max_length=100, blank=True)
    total_pages = models.IntegerField(
        validators=[MinValueValidator(1, "Books must have at least 1 page")]
    )
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        validators=[
            MinValueValidator(1.0, "Minimum rating is 1"),
            MaxValueValidator(5.0, "Maximum rating is 5")
        ],
        null=True,
        blank=True
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the Book model
        """
        return f"{self.title} by {self.author}"

    class Meta:
        """
        Metadata for the Book model
        """
        ordering = ['-created_at']  # Order by most recently added
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
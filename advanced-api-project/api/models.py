from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Author model representing a book author.
    
    This model stores basic information about authors who have written books.
    Each author can have multiple books associated with them through a 
    one-to-many relationship (one author can write many books).
    
    Fields:
        name (CharField): The full name of the author (max 100 characters)
    """
    name = models.CharField(max_length=100, help_text="The full name of the author")
    
    def __str__(self):
        """Return string representation of the author."""
        return self.name
    
    class Meta:
        ordering = ['name']  # Order authors alphabetically by name
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(models.Model):
    """
    Book model representing a published book.
    
    This model stores information about books including their title, 
    publication year, and the author who wrote them. Each book is 
    linked to exactly one author through a foreign key relationship,
    establishing a many-to-one relationship (many books to one author).
    
    Fields:
        title (CharField): The title of the book (max 200 characters)
        publication_year (IntegerField): The year the book was published
        author (ForeignKey): Reference to the Author who wrote this book
    
    Relationships:
        - Many-to-One with Author: Each book has one author, 
          but an author can have many books
        - When an author is deleted, all their books are also deleted (CASCADE)
    """
    title = models.CharField(max_length=200, help_text="The title of the book")
    publication_year = models.IntegerField(help_text="The year the book was published")
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        help_text="The author who wrote this book"
    )
    
    def __str__(self):
        """Return string representation of the book."""
        return f"{self.title} ({self.publication_year}) by {self.author.name}"
    
    class Meta:
        ordering = ['-publication_year', 'title']  # Order by year (newest first), then title
        verbose_name = "Book"
        verbose_name_plural = "Books"
        # Ensure no duplicate books (same title and author)
        unique_together = ['title', 'author']

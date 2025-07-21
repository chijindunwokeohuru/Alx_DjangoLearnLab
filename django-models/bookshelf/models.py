from django.db import models

class Book(models.Model):
    """A model representing a book in the library."""
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    def __str__(self):
        """Return a string representation of the book."""
        return f"{self.title} by {self.author} ({self.publication_year})"
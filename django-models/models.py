from django.db import models

# Advanced Django Model Relationships
# These models demonstrate ForeignKey, ManyToMany, and OneToOne relationships

class Author(models.Model):
    """Model representing an author"""
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


class Library(models.Model):
    """Model representing a library"""
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)
    
    def __str__(self):
        return self.name


class Librarian(models.Model):
    """Model representing a librarian"""
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
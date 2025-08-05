from django.contrib import admin
from .models import Author, Book

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Author model.
    
    Provides an enhanced admin interface for managing authors with
    search functionality and related book information.
    """
    list_display = ['name', 'book_count']
    search_fields = ['name']
    ordering = ['name']
    
    def book_count(self, obj):
        """Display the number of books by this author."""
        return obj.books.count()
    book_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for Book model.
    
    Provides an enhanced admin interface for managing books with
    filtering, search, and organized display options.
    """
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_year', 'title']
    list_select_related = ['author']  # Optimize database queries

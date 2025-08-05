"""
URL configuration for the API app.

This module defines URL patterns for all API endpoints including:
- Book CRUD operations
- Author views
- Custom API endpoints
- Statistical endpoints

URL Patterns:
    /api/books/ - List all books (GET)
    /api/books/<int:pk>/ - Get book detail (GET)
    /api/books/create/ - Create new book (POST)
    /api/books/<int:pk>/update/ - Update book (PUT/PATCH)
    /api/books/<int:pk>/delete/ - Delete book (DELETE)
    /api/authors/ - List all authors (GET)
    /api/authors/<int:pk>/ - Get author detail (GET)
    /api/books/stats/ - Get book statistics (GET)
    /api/my-books/ - Get user's books (GET) [Authenticated]
"""

from django.urls import path
from . import views

# URL namespace for the API app
app_name = 'api'

urlpatterns = [
    # Book CRUD endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Author endpoints
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Custom endpoints
    path('books/stats/', views.book_stats, name='book-stats'),
    path('my-books/', views.my_books, name='my-books'),
]

"""
URL Pattern Documentation:

1. Book CRUD Operations:
   - GET /api/books/ 
     * Returns paginated list of all books
     * Supports filtering: ?author=1&publication_year=2020
     * Supports searching: ?search=harry potter
     * Supports ordering: ?ordering=-publication_year,title
     * Custom filters: ?year_from=2000&year_to=2020
   
   - GET /api/books/<id>/
     * Returns detailed information about a specific book
     * Includes author information through nested serialization
   
   - POST /api/books/create/
     * Creates a new book (requires authentication)
     * Request body: {"title": "Book Title", "publication_year": 2023, "author": 1}
     * Returns created book data with success message
   
   - PUT/PATCH /api/books/<id>/update/
     * Updates an existing book (requires authentication)
     * PUT: Full update (all fields required)
     * PATCH: Partial update (only specified fields)
     * Returns updated book data with success message
   
   - DELETE /api/books/<id>/delete/
     * Deletes a book (requires authentication)
     * Returns confirmation message with deleted book info

2. Author Operations:
   - GET /api/authors/
     * Returns list of all authors with their books
     * Supports searching: ?search=author name
     * Supports ordering: ?ordering=name
   
   - GET /api/authors/<id>/
     * Returns detailed author information with all their books

3. Custom Endpoints:
   - GET /api/books/stats/
     * Returns statistical information about books
     * Includes total counts, latest/oldest books, books by decade
   
   - GET /api/my-books/
     * Returns books associated with authenticated user
     * Requires authentication

Permission Summary:
- Public Access (AllowAny): Book list, book detail, author list, author detail, book stats
- Authenticated Only (IsAuthenticated): Book create, book update, book delete, my books

Response Formats:
- Success responses include: message, data, status
- Error responses include: message, errors, status
- List responses are paginated
- Detail responses include related data through serialization
"""

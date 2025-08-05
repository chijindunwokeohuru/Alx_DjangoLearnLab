from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from rest_framework import filters

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, SimpleAuthorSerializer, SimpleBookSerializer

# Create your views here.

class BookListView(generics.ListAPIView):
    """
    Generic ListView for retrieving all books with advanced filtering, searching, and ordering.
    
    This view provides read-only access to all books in the database with comprehensive
    query capabilities for filtering, searching, and ordering results.
    
    Permissions:
        - Read-only access for all users (authenticated and unauthenticated)
    
    Features:
        - Returns paginated list of all books
        - Supports filtering by author, publication year, and custom date ranges
        - Supports search by title and author name
        - Supports ordering by multiple fields
        - Custom filtering for publication year ranges
    
    Query Parameters:
        Filtering:
            ?author=<author_id> - Filter by specific author ID
            ?publication_year=<year> - Filter by specific publication year
            ?year_from=<year> - Filter books published from this year onwards
            ?year_to=<year> - Filter books published up to this year
            
        Searching:
            ?search=<query> - Search in book title and author name
            
        Ordering:
            ?ordering=<field> - Order by field (title, publication_year, author__name)
            ?ordering=-<field> - Reverse order (prefix with -)
            ?ordering=<field1>,<field2> - Multiple field ordering
    
    Examples:
        GET /api/books/?author=1&publication_year=2020
        GET /api/books/?search=harry potter
        GET /api/books/?ordering=-publication_year,title
        GET /api/books/?year_from=2000&year_to=2020
        GET /api/books/?search=tolkien&ordering=title
    
    URL: GET /api/books/
    """
    queryset = Book.objects.all().select_related('author')  # Optimize queries
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    
    # Step 1: Set Up Filtering - Configure filter backends
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Step 1: Filtering Configuration
    # Allow filtering by author (FK), publication_year, and title
    filterset_fields = {
        'author': ['exact'],  # Filter by exact author ID
        'publication_year': ['exact', 'gte', 'lte'],  # Exact year, greater/less than
        'title': ['icontains'],  # Case-insensitive partial match
    }
    
    # Step 2: Search Functionality Configuration
    # Enable search across title and author name with case-insensitive matching
    search_fields = ['title', 'author__name']
    
    # Step 3: Ordering Configuration  
    # Allow ordering by all major fields
    ordering_fields = ['title', 'publication_year', 'author__name', 'id']
    ordering = ['-publication_year', 'title']  # Default ordering: newest first, then alphabetical
    
    def get_queryset(self):
        """
        Custom queryset filtering for advanced filtering capabilities.
        
        Implements custom filtering logic beyond basic DjangoFilterBackend:
        - Publication year range filtering (year_from, year_to)
        - Additional custom filters can be added here
        
        Returns:
            QuerySet: Filtered queryset based on query parameters
        """
        queryset = super().get_queryset()
        
        # Custom filter: Publication year range
        year_from = self.request.query_params.get('year_from')
        year_to = self.request.query_params.get('year_to')
        
        if year_from:
            try:
                year_from = int(year_from)
                queryset = queryset.filter(publication_year__gte=year_from)
            except ValueError:
                pass  # Ignore invalid year format
                
        if year_to:
            try:
                year_to = int(year_to)
                queryset = queryset.filter(publication_year__lte=year_to)
            except ValueError:
                pass  # Ignore invalid year format
        
        # Custom filter: Books by specific author name (case-insensitive)
        author_name = self.request.query_params.get('author_name')
        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)
            
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Override list method to provide additional context in response.
        
        Returns filtering and ordering information along with results.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Get query parameters for context
        query_params = dict(request.query_params)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            
            # Add filtering context to response
            response.data['filters_applied'] = {
                'search': request.query_params.get('search', None),
                'ordering': request.query_params.get('ordering', self.ordering),
                'filters': {k: v for k, v in query_params.items() 
                           if k not in ['search', 'ordering', 'page']}
            }
            response.data['available_filters'] = {
                'author': 'Filter by author ID (exact match)',
                'publication_year': 'Filter by publication year (exact, gte, lte)',
                'title': 'Filter by title (case-insensitive partial match)',
                'year_from': 'Custom filter: books from this year onwards',
                'year_to': 'Custom filter: books up to this year',
                'author_name': 'Custom filter: books by author name (partial match)'
            }
            response.data['available_search'] = 'Search in: title, author name'
            response.data['available_ordering'] = 'Order by: title, publication_year, author__name, id (prefix with - for descending)'
            
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'filters_applied': {
                'search': request.query_params.get('search', None),
                'ordering': request.query_params.get('ordering', self.ordering),
                'filters': {k: v for k, v in query_params.items() 
                           if k not in ['search', 'ordering']}
            }
        })


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single book by ID.
    
    This view provides read-only access to a specific book instance.
    
    Permissions:
        - Read-only access for all users (authenticated and unauthenticated)
    
    Features:
        - Returns detailed information about a specific book
        - Includes related author information
        - Returns 404 if book doesn't exist
    
    URL: GET /api/books/<int:pk>/
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    
    def get_object(self):
        """
        Override to add custom object retrieval logic if needed.
        """
        obj = super().get_object()
        # Could add custom logic here (e.g., logging, analytics)
        return obj


class BookCreateView(generics.CreateAPIView):
    """
    Generic CreateView for adding a new book.
    
    This view allows authenticated users to create new book instances.
    
    Permissions:
        - Create access restricted to authenticated users only
    
    Features:
        - Validates book data using BookSerializer
        - Enforces custom validation rules (e.g., publication year)
        - Returns created book data upon successful creation
        - Returns detailed error messages for validation failures
    
    URL: POST /api/books/create/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def perform_create(self, serializer):
        """
        Customize the creation process.
        
        This method is called after validation but before saving.
        Can be used to set additional fields or perform custom logic.
        """
        # Example: Set additional metadata or perform logging
        book = serializer.save()
        
        # Log book creation (in a real app, use proper logging)
        print(f"New book created: {book.title} by {book.author.name}")
        
        return book
    
    def create(self, request, *args, **kwargs):
        """
        Override create method to provide custom response formatting.
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            # Custom success response
            response_data = {
                'message': 'Book created successfully',
                'book': serializer.data,
                'status': 'success'
            }
            
            return Response(
                response_data, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        else:
            # Custom error response
            response_data = {
                'message': 'Book creation failed',
                'errors': serializer.errors,
                'status': 'error'
            }
            
            return Response(
                response_data, 
                status=status.HTTP_400_BAD_REQUEST
            )


class BookUpdateView(generics.UpdateAPIView):
    """
    Generic UpdateView for modifying an existing book.
    
    This view allows authenticated users to update existing book instances.
    Supports both PUT (full update) and PATCH (partial update) methods.
    
    Permissions:
        - Update access restricted to authenticated users only
    
    Features:
        - Validates updated book data using BookSerializer
        - Supports partial updates (PATCH method)
        - Enforces custom validation rules
        - Returns updated book data upon successful update
        - Returns detailed error messages for validation failures
    
    URL: PUT/PATCH /api/books/<int:pk>/update/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def perform_update(self, serializer):
        """
        Customize the update process.
        
        This method is called after validation but before saving.
        """
        book = serializer.save()
        
        # Log book update
        print(f"Book updated: {book.title} by {book.author.name}")
        
        return book
    
    def update(self, request, *args, **kwargs):
        """
        Override update method to provide custom response formatting.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            
            # Custom success response
            response_data = {
                'message': 'Book updated successfully',
                'book': serializer.data,
                'status': 'success'
            }
            
            return Response(response_data)
        else:
            # Custom error response
            response_data = {
                'message': 'Book update failed',
                'errors': serializer.errors,
                'status': 'error'
            }
            
            return Response(
                response_data, 
                status=status.HTTP_400_BAD_REQUEST
            )


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic DeleteView for removing a book.
    
    This view allows authenticated users to delete existing book instances.
    
    Permissions:
        - Delete access restricted to authenticated users only
    
    Features:
        - Permanently removes book from database
        - Returns confirmation message upon successful deletion
        - Returns 404 if book doesn't exist
        - Cascades to remove related data if applicable
    
    URL: DELETE /api/books/<int:pk>/delete/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def perform_destroy(self, instance):
        """
        Customize the deletion process.
        
        This method is called before the instance is deleted.
        """
        # Log book deletion
        print(f"Book deleted: {instance.title} by {instance.author.name}")
        
        # Perform the actual deletion
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to provide custom response formatting.
        """
        instance = self.get_object()
        book_info = {
            'id': instance.id,
            'title': instance.title,
            'author': instance.author.name
        }
        
        self.perform_destroy(instance)
        
        # Custom success response
        response_data = {
            'message': 'Book deleted successfully',
            'deleted_book': book_info,
            'status': 'success'
        }
        
        return Response(
            response_data, 
            status=status.HTTP_200_OK
        )


# Additional views for Author model

class AuthorListView(generics.ListAPIView):
    """
    Generic ListView for retrieving all authors with their books.
    
    This view provides read-only access to all authors in the database,
    including their associated books through nested serialization.
    
    Permissions:
        - Read-only access for all users
    
    URL: GET /api/authors/
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single author with their books.
    
    URL: GET /api/authors/<int:pk>/
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


# Custom API Views (function-based examples)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def book_stats(request):
    """
    Custom API view to return book statistics.
    
    This demonstrates how to create custom endpoints that don't
    follow the standard CRUD pattern.
    
    URL: GET /api/books/stats/
    """
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    latest_book = Book.objects.order_by('-publication_year').first()
    oldest_book = Book.objects.order_by('publication_year').first()
    
    # Books per decade
    from django.db.models import Count, IntegerField
    from django.db.models.functions import Extract
    
    books_by_decade = (
        Book.objects
        .extra(select={'decade': '(publication_year / 10) * 10'})
        .values('decade')
        .annotate(count=Count('id'))
        .order_by('decade')
    )
    
    stats = {
        'total_books': total_books,
        'total_authors': total_authors,
        'latest_book': {
            'title': latest_book.title if latest_book else None,
            'year': latest_book.publication_year if latest_book else None,
            'author': latest_book.author.name if latest_book else None
        },
        'oldest_book': {
            'title': oldest_book.title if oldest_book else None,
            'year': oldest_book.publication_year if oldest_book else None,
            'author': oldest_book.author.name if oldest_book else None
        },
        'books_by_decade': list(books_by_decade)
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_books(request):
    """
    Custom view to return books created by the current user.
    
    This is an example of user-specific data retrieval.
    In a real application, you might track who created each book.
    
    URL: GET /api/my-books/
    """
    # This is a placeholder - in a real app, you'd have user tracking
    response_data = {
        'message': 'This endpoint would return books created by the authenticated user',
        'user': request.user.username,
        'note': 'User tracking not implemented in this demo'
    }
    
    return Response(response_data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def book_update_endpoint(request):
    """
    Function-based view for updating books.
    Expects book ID in request data.
    
    URL: PUT/PATCH /api/books/update/
    """
    book_id = request.data.get('id')
    if not book_id:
        return Response({
            'message': 'Book ID is required',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({
            'message': 'Book not found',
            'status': 'error'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Book updated successfully',
            'book': serializer.data,
            'status': 'success'
        })
    else:
        return Response({
            'message': 'Book update failed',
            'errors': serializer.errors,
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def book_delete_endpoint(request):
    """
    Function-based view for deleting books.
    Expects book ID in request data.
    
    URL: DELETE /api/books/delete/
    """
    book_id = request.data.get('id')
    if not book_id:
        return Response({
            'message': 'Book ID is required',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        book = Book.objects.get(pk=book_id)
        book_data = BookSerializer(book).data
        book.delete()
        return Response({
            'message': 'Book deleted successfully',
            'deleted_book': book_data,
            'status': 'success'
        })
    except Book.DoesNotExist:
        return Response({
            'message': 'Book not found',
            'status': 'error'
        }, status=status.HTTP_404_NOT_FOUND)

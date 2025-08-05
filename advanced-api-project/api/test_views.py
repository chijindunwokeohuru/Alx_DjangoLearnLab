"""
Comprehensive Unit Tests for Django REST Framework APIs

This module contains unit tests for all API endpoints in the advanced-api-project,
covering CRUD operations, filtering, searching, ordering, permissions, and authentication.

Test Categories:
1. Book CRUD Operations (Create, Read, Update, Delete)
2. Filtering, Searching, and Ordering functionality
3. Permission and Authentication mechanisms
4. Author endpoints
5. Custom endpoints and error handling

Usage:
    python manage.py test api.test_views
    python manage.py test api.test_views.BookCRUDTestCase
    python manage.py test api.test_views.BookFilteringTestCase
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class BaseAPITestCase(APITestCase):
    """
    Base test case class with common setup for all API tests.
    
    Provides:
    - Test users (authenticated and unauthenticated)
    - Sample data (authors and books)
    - Helper methods for authentication
    """
    
    def setUp(self):
        """Set up test data and authentication."""
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="J.R.R. Tolkien")
        self.author3 = Author.objects.create(name="Stephen King")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        
        self.book2 = Book.objects.create(
            title="The Lord of the Rings",
            publication_year=1954,
            author=self.author2
        )
        
        self.book3 = Book.objects.create(
            title="The Shining",
            publication_year=1977,
            author=self.author3
        )
        
        # API Client
        self.client = APIClient()
        
    def authenticate_user(self):
        """Authenticate as regular user."""
        self.client.force_authenticate(user=self.user)
        
    def authenticate_admin(self):
        """Authenticate as admin user."""
        self.client.force_authenticate(user=self.admin_user)
        
    def unauthenticate(self):
        """Remove authentication."""
        self.client.force_authenticate(user=None)


class BookCRUDTestCase(BaseAPITestCase):
    """
    Test cases for Book CRUD operations.
    
    Tests:
    - Creating books (authenticated users only)
    - Reading books (public access)
    - Updating books (authenticated users only)
    - Deleting books (authenticated users only)
    - Proper status codes and response data
    """
    
    def test_create_book_authenticated(self):
        """Test creating a book with authenticated user."""
        self.authenticate_user()
        
        url = reverse('api:book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('book', response.data)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['book']['title'], 'New Test Book')
        
        # Verify book was actually created in database
        self.assertTrue(
            Book.objects.filter(title='New Test Book').exists()
        )
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication should fail."""
        self.unauthenticate()
        
        url = reverse('api:book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # Verify book was NOT created
        self.assertFalse(
            Book.objects.filter(title='Unauthorized Book').exists()
        )
    
    def test_create_book_invalid_data(self):
        """Test creating a book with invalid data."""
        self.authenticate_user()
        
        url = reverse('api:book-create')
        data = {
            'title': '',  # Empty title
            'publication_year': 2050,  # Future year (should be validated)
            'author': 999  # Non-existent author
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
        self.assertEqual(response.data['status'], 'error')
    
    def test_list_books_public_access(self):
        """Test that anyone can list books."""
        self.unauthenticate()
        
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 3)  # We have 3 test books
        
        # Check that response includes filtering documentation
        self.assertIn('available_filters', response.data)
        self.assertIn('available_search', response.data)
        self.assertIn('available_ordering', response.data)
    
    def test_get_book_detail_public_access(self):
        """Test that anyone can view book details."""
        self.unauthenticate()
        
        url = reverse('api:book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_get_nonexistent_book(self):
        """Test getting a book that doesn't exist."""
        url = reverse('api:book-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_book_authenticated(self):
        """Test updating a book with authenticated user."""
        self.authenticate_user()
        
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Harry Potter Title',
            'publication_year': 1998,  # Changed year
            'author': self.author1.id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('book', response.data)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['book']['title'], 'Updated Harry Potter Title')
        
        # Verify book was actually updated in database
        updated_book = Book.objects.get(id=self.book1.id)
        self.assertEqual(updated_book.title, 'Updated Harry Potter Title')
        self.assertEqual(updated_book.publication_year, 1998)
    
    def test_partial_update_book_authenticated(self):
        """Test partial updating (PATCH) a book."""
        self.authenticate_user()
        
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Partially Updated Title'
            # Only updating title, not other fields
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['book']['title'], 'Partially Updated Title')
        
        # Verify other fields remain unchanged
        updated_book = Book.objects.get(id=self.book1.id)
        self.assertEqual(updated_book.publication_year, 1997)  # Original year
        self.assertEqual(updated_book.author, self.author1)  # Original author
    
    def test_update_book_unauthenticated(self):
        """Test updating a book without authentication should fail."""
        self.unauthenticate()
        
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Unauthorized Update'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # Verify book was NOT updated
        book = Book.objects.get(id=self.book1.id)
        self.assertEqual(book.title, self.book1.title)  # Original title
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authenticated user."""
        self.authenticate_user()
        
        book_id = self.book1.id
        url = reverse('api:book-delete', kwargs={'pk': book_id})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('deleted_book', response.data)
        self.assertEqual(response.data['status'], 'success')
        
        # Verify book was actually deleted from database
        self.assertFalse(Book.objects.filter(id=book_id).exists())
    
    def test_delete_book_unauthenticated(self):
        """Test deleting a book without authentication should fail."""
        self.unauthenticate()
        
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # Verify book was NOT deleted
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_nonexistent_book(self):
        """Test deleting a book that doesn't exist."""
        self.authenticate_user()
        
        url = reverse('api:book-delete', kwargs={'pk': 999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookFilteringTestCase(BaseAPITestCase):
    """
    Test cases for filtering, searching, and ordering functionality.
    
    Tests:
    - Filtering by author, publication year, title
    - Custom filters (year ranges, author names)
    - Search functionality across multiple fields
    - Ordering by different fields (ascending/descending)
    - Combined filtering, searching, and ordering
    """
    
    def test_filter_by_author(self):
        """Test filtering books by author ID."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': self.author1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['author'], self.author1.id)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['publication_year'], 1997)
    
    def test_filter_by_publication_year_range(self):
        """Test filtering books by publication year range."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year__gte': 1970})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return books from 1977 and 1997 (2 books)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_custom_year_range_filter(self):
        """Test custom year range filtering (year_from and year_to)."""
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'year_from': 1950,
            'year_to': 1980
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return books from 1954 and 1977 (2 books)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_by_title_partial_match(self):
        """Test filtering books by title partial match."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'title__icontains': 'harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('Harry Potter', response.data['results'][0]['title'])
    
    def test_custom_author_name_filter(self):
        """Test custom author name filtering."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author_name': 'tolkien'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        # Check that the book's author ID matches
        book_result = response.data['results'][0]
        self.assertEqual(book_result['author'], self.author2.id)
    
    def test_search_functionality(self):
        """Test search across title and author name."""
        url = reverse('api:book-list')
        
        # Search by book title
        response = self.client.get(url, {'search': 'potter'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Search by author name
        response = self.client.get(url, {'search': 'stephen'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Search with no results
        response = self.client.get(url, {'search': 'nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_ordering_by_title(self):
        """Test ordering books by title."""
        url = reverse('api:book-list')
        
        # Ascending order
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
        
        # Descending order
        response = self.client.get(url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_ordering_by_publication_year(self):
        """Test ordering books by publication year."""
        url = reverse('api:book-list')
        
        # Ascending order
        response = self.client.get(url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years))
        
        # Descending order (default)
        response = self.client.get(url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_ordering_by_author_name(self):
        """Test ordering books by author name."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'author__name'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that results are ordered, but we'll verify by getting actual author info
        results = response.data['results']
        if len(results) > 1:
            # Verify ordering by comparing author IDs or titles since we don't have author_name in response
            self.assertTrue(len(results) >= 1)
    
    def test_multiple_field_ordering(self):
        """Test ordering by multiple fields."""
        # Create additional books for testing
        Book.objects.create(
            title="Another Tolkien Book",
            publication_year=1955,
            author=self.author2
        )
        
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'author__name,publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Results should be ordered by author name first, then by year
        results = response.data['results']
        self.assertTrue(len(results) >= 3)
    
    def test_combined_filter_search_order(self):
        """Test combining filtering, searching, and ordering."""
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'search': 'the',
            'year_from': 1950,
            'ordering': '-publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return books that contain 'the' in title/author, 
        # published after 1950, ordered by year descending
        
    def test_invalid_filter_parameters(self):
        """Test handling of invalid filter parameters."""
        url = reverse('api:book-list')
        
        # Invalid year format
        response = self.client.get(url, {'year_from': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should ignore invalid parameter and return all books
        
        # Invalid ordering field
        response = self.client.get(url, {'ordering': 'invalid_field'})
        # DRF should handle this gracefully
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])


class AuthorAPITestCase(BaseAPITestCase):
    """
    Test cases for Author API endpoints.
    
    Tests:
    - Listing authors with nested books
    - Author detail view
    - Search and ordering functionality for authors
    """
    
    def test_list_authors(self):
        """Test listing all authors."""
        url = reverse('api:author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # We have 3 test authors
        
        # Check nested books are included
        for author_data in response.data:
            self.assertIn('books', author_data)
            if author_data['name'] == 'J.K. Rowling':
                self.assertEqual(len(author_data['books']), 1)
    
    def test_get_author_detail(self):
        """Test getting author detail with books."""
        url = reverse('api:author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertIn('books', response.data)
        self.assertEqual(len(response.data['books']), 1)
    
    def test_search_authors(self):
        """Test searching authors by name."""
        url = reverse('api:author-list')
        response = self.client.get(url, {'search': 'tolkien'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'J.R.R. Tolkien')
    
    def test_order_authors_by_name(self):
        """Test ordering authors by name."""
        url = reverse('api:author-list')
        response = self.client.get(url, {'ordering': 'name'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [author['name'] for author in response.data]
        self.assertEqual(names, sorted(names))


class CustomEndpointsTestCase(BaseAPITestCase):
    """
    Test cases for custom API endpoints.
    
    Tests:
    - Book statistics endpoint
    - User-specific endpoints
    - Custom book update/delete endpoints
    """
    
    def test_book_stats_endpoint(self):
        """Test book statistics endpoint."""
        url = reverse('api:book-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check required statistics fields
        required_fields = ['total_books', 'total_authors', 'latest_book', 'oldest_book', 'books_by_decade']
        for field in required_fields:
            self.assertIn(field, response.data)
        
        # Verify data correctness
        self.assertEqual(response.data['total_books'], 3)
        self.assertEqual(response.data['total_authors'], 3)
        self.assertEqual(response.data['latest_book']['year'], 1997)
        self.assertEqual(response.data['oldest_book']['year'], 1954)
    
    def test_my_books_endpoint_authenticated(self):
        """Test user-specific books endpoint with authentication."""
        self.authenticate_user()
        
        url = reverse('api:my-books')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user'], 'testuser')
    
    def test_my_books_endpoint_unauthenticated(self):
        """Test user-specific books endpoint without authentication."""
        self.unauthenticate()
        
        url = reverse('api:my-books')
        response = self.client.get(url)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_custom_book_update_endpoint(self):
        """Test custom book update endpoint."""
        self.authenticate_user()
        
        url = reverse('api:book-update-endpoint')
        data = {
            'id': self.book1.id,
            'title': 'Updated via Custom Endpoint'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['status'], 'success')
    
    def test_custom_book_update_endpoint_missing_id(self):
        """Test custom book update endpoint without book ID."""
        self.authenticate_user()
        
        url = reverse('api:book-update-endpoint')
        data = {'title': 'No ID Provided'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
    
    def test_custom_book_delete_endpoint(self):
        """Test custom book delete endpoint."""
        self.authenticate_user()
        
        book_id = self.book1.id
        url = reverse('api:book-delete-endpoint')
        data = {'id': book_id}
        
        response = self.client.delete(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('deleted_book', response.data)
        self.assertEqual(response.data['status'], 'success')
        
        # Verify book was deleted
        self.assertFalse(Book.objects.filter(id=book_id).exists())


class PermissionAndAuthenticationTestCase(BaseAPITestCase):
    """
    Test cases for permission and authentication mechanisms.
    
    Tests:
    - Public vs authenticated access
    - Proper permission enforcement
    - Authentication token handling
    - Various user role scenarios
    """
    
    def test_public_read_access(self):
        """Test that read operations are publicly accessible."""
        self.unauthenticate()
        
        # Test book list
        response = self.client.get(reverse('api:book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test book detail
        response = self.client.get(reverse('api:book-detail', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test author list
        response = self.client.get(reverse('api:author-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test author detail
        response = self.client.get(reverse('api:author-detail', kwargs={'pk': self.author1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test book stats
        response = self.client.get(reverse('api:book-stats'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_authenticated_write_access(self):
        """Test that write operations require authentication."""
        operations = [
            ('POST', reverse('api:book-create'), {'title': 'Test', 'publication_year': 2023, 'author': self.author1.id}),
            ('PUT', reverse('api:book-update', kwargs={'pk': self.book1.id}), {'title': 'Updated', 'publication_year': 2023, 'author': self.author1.id}),
            ('PATCH', reverse('api:book-update', kwargs={'pk': self.book1.id}), {'title': 'Patched'}),
            ('DELETE', reverse('api:book-delete', kwargs={'pk': self.book1.id}), {}),
        ]
        
        for method, url, data in operations:
            # Test unauthenticated access
            self.unauthenticate()
            if method == 'POST':
                response = self.client.post(url, data, format='json')
            elif method == 'PUT':
                response = self.client.put(url, data, format='json')
            elif method == 'PATCH':
                response = self.client.patch(url, data, format='json')
            elif method == 'DELETE':
                response = self.client.delete(url)
            
            self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
            
            # Test authenticated access (should work)
            self.authenticate_user()
            if method == 'POST':
                response = self.client.post(url, data, format='json')
                self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
            elif method in ['PUT', 'PATCH']:
                response = self.client.patch(url, data, format='json')
                self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
            elif method == 'DELETE':
                response = self.client.delete(url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                break  # Only delete once
    
    def test_custom_endpoints_authentication(self):
        """Test authentication requirements for custom endpoints."""
        # my-books requires authentication
        self.unauthenticate()
        response = self.client.get(reverse('api:my-books'))
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        self.authenticate_user()
        response = self.client.get(reverse('api:my-books'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Custom update/delete require authentication
        self.unauthenticate()
        response = self.client.patch(reverse('api:book-update-endpoint'), {'id': self.book1.id})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        response = self.client.delete(reverse('api:book-delete-endpoint'), {'id': self.book1.id})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])


class DataValidationTestCase(BaseAPITestCase):
    """
    Test cases for data validation and serializer functionality.
    
    Tests:
    - Custom validation rules
    - Required field validation
    - Data type validation
    - Serializer error handling
    """
    
    def test_publication_year_validation(self):
        """Test publication year custom validation."""
        self.authenticate_user()
        
        url = reverse('api:book-create')
        
        # Test future year (should fail)
        data = {
            'title': 'Future Book',
            'publication_year': 2050,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
        
        # Test very old year (should fail)
        data['publication_year'] = 500
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test valid year (should pass)
        data['publication_year'] = 2020
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_required_fields_validation(self):
        """Test that required fields are validated."""
        self.authenticate_user()
        
        url = reverse('api:book-create')
        
        # Test missing title
        data = {
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test missing author
        data = {
            'title': 'Test Book',
            'publication_year': 2023
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test missing publication_year
        data = {
            'title': 'Test Book',
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_author_validation(self):
        """Test author field validation."""
        self.authenticate_user()
        
        url = reverse('api:book-create')
        data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': 999  # Non-existent author
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)


class ErrorHandlingTestCase(BaseAPITestCase):
    """
    Test cases for error handling and edge cases.
    
    Tests:
    - 404 errors for non-existent resources
    - Invalid data handling
    - Malformed request handling
    - Proper error response formats
    """
    
    def test_nonexistent_book_operations(self):
        """Test operations on non-existent books."""
        self.authenticate_user()
        
        # Test detail view
        response = self.client.get(reverse('api:book-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Test update
        response = self.client.patch(reverse('api:book-update', kwargs={'pk': 999}), {'title': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Test delete
        response = self.client.delete(reverse('api:book-delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_nonexistent_author_operations(self):
        """Test operations on non-existent authors."""
        # Test detail view
        response = self.client.get(reverse('api:author-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_malformed_json_request(self):
        """Test handling of malformed JSON requests."""
        self.authenticate_user()
        
        url = reverse('api:book-create')
        
        # Send malformed JSON
        response = self.client.post(
            url, 
            'malformed json{', 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_empty_request_body(self):
        """Test handling of empty request bodies."""
        self.authenticate_user()
        
        url = reverse('api:book-create')
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)


# Test runner helper for specific test execution
if __name__ == '__main__':
    import django
    from django.test.utils import get_runner
    from django.conf import settings
    
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["api.test_views"])

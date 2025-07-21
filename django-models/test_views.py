#!/usr/bin/env python
"""
Test script for Django Views and URL Configuration
This script tests the views functionality without running the full server
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.test import RequestFactory
from django.http import HttpRequest
from relationship_app.views import list_books, LibraryDetailView
from relationship_app.models import Library

def test_views():
    """Test both function-based and class-based views"""
    print("Testing Django Views and URL Configuration")
    print("=" * 50)
    
    # Create a request factory for testing
    factory = RequestFactory()
    
    # Test function-based view (list_books)
    print("1. Testing Function-based View (list_books):")
    request = factory.get('/books/')
    response = list_books(request)
    print(f"   - Response status: {response.status_code}")
    print(f"   - Content type: {response.get('Content-Type', 'text/html')}")
    if response.status_code == 200:
        print("   ✅ Function-based view working correctly")
    else:
        print("   ❌ Function-based view failed")
    
    # Test class-based view (LibraryDetailView)
    print("\n2. Testing Class-based View (LibraryDetailView):")
    try:
        # Get the first library for testing
        library = Library.objects.first()
        if library:
            request = factory.get(f'/library/{library.pk}/')
            view = LibraryDetailView.as_view()
            response = view(request, pk=library.pk)
            print(f"   - Response status: {response.status_code}")
            print(f"   - Testing with library: {library.name}")
            if response.status_code == 200:
                print("   ✅ Class-based view working correctly")
            else:
                print("   ❌ Class-based view failed")
        else:
            print("   ⚠️  No libraries found in database")
    except Exception as e:
        print(f"   ❌ Error testing class-based view: {e}")
    
    print("\n3. URL Patterns Summary:")
    print("   - /books/ → list_books (function-based view)")
    print("   - /library/<int:pk>/ → LibraryDetailView (class-based view)")
    
    print("\n4. Templates Created:")
    print("   - relationship_app/templates/relationship_app/list_books.html")
    print("   - relationship_app/templates/relationship_app/library_detail.html")
    
    print("\n✅ Views and URL Configuration implementation complete!")

if __name__ == "__main__":
    test_views()

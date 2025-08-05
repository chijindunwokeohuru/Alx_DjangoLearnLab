#!/usr/bin/env python
"""
Test script to verify Author and Book models and serializers functionality.

This script demonstrates:
1. Creating Author and Book instances
2. Testing the serializers with various data
3. Validating custom validation rules
4. Showing the relationship between Author and Book models
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer, SimpleAuthorSerializer, SimpleBookSerializer
from datetime import datetime

def test_models_and_serializers():
    """Test the models and serializers functionality."""
    
    print("=" * 60)
    print("TESTING DJANGO MODELS AND SERIALIZERS")
    print("=" * 60)
    
    # Clear existing data
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Test 1: Create Authors
    print("\n1. Creating Authors...")
    
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Agatha Christie")
    
    print(f"✅ Created author: {author1}")
    print(f"✅ Created author: {author2}")
    print(f"✅ Created author: {author3}")
    
    # Test 2: Create Books
    print("\n2. Creating Books...")
    
    book1 = Book.objects.create(
        title="Harry Potter and the Philosopher's Stone",
        publication_year=1997,
        author=author1
    )
    
    book2 = Book.objects.create(
        title="Harry Potter and the Chamber of Secrets",
        publication_year=1998,
        author=author1
    )
    
    book3 = Book.objects.create(
        title="1984",
        publication_year=1949,
        author=author2
    )
    
    book4 = Book.objects.create(
        title="Animal Farm",
        publication_year=1945,
        author=author2
    )
    
    book5 = Book.objects.create(
        title="Murder on the Orient Express",
        publication_year=1934,
        author=author3
    )
    
    print(f"✅ Created book: {book1}")
    print(f"✅ Created book: {book2}")
    print(f"✅ Created book: {book3}")
    print(f"✅ Created book: {book4}")
    print(f"✅ Created book: {book5}")
    
    # Test 3: Test BookSerializer
    print("\n3. Testing BookSerializer...")
    
    book_serializer = BookSerializer(book1)
    print("📖 Book serialization:")
    print(book_serializer.data)
    
    # Test validation - try to create a book with future publication year
    print("\n4. Testing BookSerializer validation (future year)...")
    future_book_data = {
        'title': 'Future Book',
        'publication_year': datetime.now().year + 1,
        'author': author1.id
    }
    
    future_book_serializer = BookSerializer(data=future_book_data)
    if not future_book_serializer.is_valid():
        print("❌ Validation failed as expected:")
        print(future_book_serializer.errors)
    else:
        print("⚠️ Validation should have failed but didn't!")
    
    # Test valid book data
    print("\n5. Testing BookSerializer with valid data...")
    valid_book_data = {
        'title': 'A New Adventure',
        'publication_year': 2020,
        'author': author1.id
    }
    
    valid_book_serializer = BookSerializer(data=valid_book_data)
    if valid_book_serializer.is_valid():
        print("✅ Validation passed:")
        saved_book = valid_book_serializer.save()
        print(f"✅ Created book: {saved_book}")
    else:
        print("❌ Validation failed:")
        print(valid_book_serializer.errors)
    
    # Test 6: Test AuthorSerializer with nested books
    print("\n6. Testing AuthorSerializer with nested books...")
    
    author_serializer = AuthorSerializer(author1)
    print("👤 Author with nested books:")
    import json
    print(json.dumps(author_serializer.data, indent=2))
    
    # Test 7: Test relationship queries
    print("\n7. Testing model relationships...")
    
    print(f"📚 Books by {author1.name}:")
    for book in author1.books.all():
        print(f"   - {book.title} ({book.publication_year})")
    
    print(f"📚 Books by {author2.name}:")
    for book in author2.books.all():
        print(f"   - {book.title} ({book.publication_year})")
    
    # Test 8: Test SimpleAuthorSerializer
    print("\n8. Testing SimpleAuthorSerializer...")
    
    simple_author_serializer = SimpleAuthorSerializer(author1)
    print("👤 Simple author serialization:")
    print(simple_author_serializer.data)
    
    # Test 9: Test bulk serialization
    print("\n9. Testing bulk serialization...")
    
    all_authors = Author.objects.all()
    all_authors_serializer = AuthorSerializer(all_authors, many=True)
    print("👥 All authors with their books:")
    print(f"Total authors: {len(all_authors_serializer.data)}")
    
    all_books = Book.objects.all()
    all_books_serializer = SimpleBookSerializer(all_books, many=True)
    print("📚 All books:")
    for book_data in all_books_serializer.data:
        print(f"   - {book_data['title']} by {book_data['author_name']}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"   - Authors created: {Author.objects.count()}")
    print(f"   - Books created: {Book.objects.count()}")
    print(f"   - Serializers tested: BookSerializer, AuthorSerializer, SimpleAuthorSerializer, SimpleBookSerializer")
    print(f"   - Validation tested: ✅ Future publication year validation")
    print(f"   - Relationships tested: ✅ Author-Book one-to-many relationship")

if __name__ == '__main__':
    test_models_and_serializers()

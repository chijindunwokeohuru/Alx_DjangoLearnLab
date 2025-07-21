import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    """
    Query all books by a specific author.
    This demonstrates ForeignKey relationship usage.
    """
    try:
        # Get the author by name
        author = Author.objects.get(name=author_name)
        
        # Query all books by this author (using ForeignKey relationship)
        books = Book.objects.filter(author=author)
        
        print(f"Books by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
        
        return books
    
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []


def list_all_books_in_library(library_name):
    """
    List all books in a library.
    This demonstrates ManyToMany relationship usage.
    """
    try:
        # Get the library by name
        library = Library.objects.get(name=library_name)
        
        # Query all books in this library (using ManyToMany relationship)
        books = library.books.all()
        
        print(f"Books in {library_name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
        
        return books
    
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    This demonstrates OneToOne relationship usage.
    """
    try:
        # Get the library by name
        library = Library.objects.get(name=library_name)
        
        # Get the librarian for this library (using OneToOne relationship)
        librarian = Librarian.objects.get(library=library)
        
        print(f"Librarian for {library_name}: {librarian.name}")
        
        return librarian
    
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}'.")
        return None


def create_sample_data():
    """
    Create some sample data to test the queries.
    """
    # Create authors
    author1 = Author.objects.get_or_create(name="J.K. Rowling")[0]
    author2 = Author.objects.get_or_create(name="George Orwell")[0]
    author3 = Author.objects.get_or_create(name="Harper Lee")[0]
    
    # Create books
    book1 = Book.objects.get_or_create(title="Harry Potter and the Philosopher's Stone", author=author1)[0]
    book2 = Book.objects.get_or_create(title="Harry Potter and the Chamber of Secrets", author=author1)[0]
    book3 = Book.objects.get_or_create(title="1984", author=author2)[0]
    book4 = Book.objects.get_or_create(title="Animal Farm", author=author2)[0]
    book5 = Book.objects.get_or_create(title="To Kill a Mockingbird", author=author3)[0]
    
    # Create libraries
    library1 = Library.objects.get_or_create(name="Central City Library")[0]
    library2 = Library.objects.get_or_create(name="Downtown Public Library")[0]
    
    # Add books to libraries (ManyToMany relationship)
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4, book5)
    
    # Create librarians
    librarian1 = Librarian.objects.get_or_create(name="Alice Johnson", library=library1)[0]
    librarian2 = Librarian.objects.get_or_create(name="Bob Smith", library=library2)[0]
    
    print("Sample data created successfully!")


if __name__ == "__main__":
    print("Django ORM Query Samples")
    print("=" * 50)
    
    # Create sample data
    create_sample_data()
    print()
    
    # Demonstrate ForeignKey relationship
    print("1. ForeignKey Relationship - Query all books by a specific author:")
    query_all_books_by_author("J.K. Rowling")
    print()
    
    # Demonstrate ManyToMany relationship
    print("2. ManyToMany Relationship - List all books in a library:")
    list_all_books_in_library("Central City Library")
    print()
    
    # Demonstrate OneToOne relationship
    print("3. OneToOne Relationship - Retrieve the librarian for a library:")
    retrieve_librarian_for_library("Central City Library")
    print()
    
    # Additional queries
    print("Additional query examples:")
    print("-" * 30)
    query_all_books_by_author("George Orwell")
    print()
    list_all_books_in_library("Downtown Public Library")
    print()
    retrieve_librarian_for_library("Downtown Public Library")
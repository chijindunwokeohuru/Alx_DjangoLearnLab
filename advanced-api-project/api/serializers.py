from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Book model.
    
    This serializer handles the serialization and deserialization of Book instances,
    including all fields of the Book model. It includes custom validation to ensure
    the publication year is not in the future.
    
    Serialized Fields:
        - id: Auto-generated primary key
        - title: Book title
        - publication_year: Year of publication (with validation)
        - author: Foreign key reference to Author (ID only in basic serialization)
    
    Custom Validation:
        - publication_year: Must not be in the future
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        This prevents users from entering unrealistic publication dates.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = datetime.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. "
                f"Current year is {current_year}, but received {value}."
            )
        
        # Additional validation: publication year should be reasonable (not before printing was invented)
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year seems too early. Please enter a reasonable publication year."
            )
            
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Author model with nested book serialization.
    
    This serializer provides a comprehensive view of an author including
    all their associated books. It uses a nested BookSerializer to 
    dynamically serialize the related books, creating a hierarchical 
    JSON structure that shows the one-to-many relationship between 
    authors and books.
    
    Serialized Fields:
        - id: Auto-generated primary key
        - name: Author's full name
        - books: Nested serialization of all books by this author
    
    Relationship Handling:
        The 'books' field uses the related_name='books' defined in the 
        Book model's foreign key to Author. This allows the serializer
        to automatically access all books written by the author through
        the reverse relationship.
    
    Usage:
        When serializing an Author instance, the output will include:
        {
            "id": 1,
            "name": "J.K. Rowling",
            "books": [
                {
                    "id": 1,
                    "title": "Harry Potter and the Philosopher's Stone",
                    "publication_year": 1997,
                    "author": 1
                },
                {
                    "id": 2,
                    "title": "Harry Potter and the Chamber of Secrets",
                    "publication_year": 1998,
                    "author": 1
                }
            ]
        }
    """
    
    # Nested serialization of related books
    # many=True because one author can have many books
    # read_only=True because we don't want to allow creation/editing of books through author serializer
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def validate_name(self, value):
        """
        Custom validation for the author name field.
        
        Ensures the author name meets basic requirements:
        - Not empty or just whitespace
        - Has reasonable length
        - Contains at least one letter
        
        Args:
            value (str): The author name to validate
            
        Returns:
            str: The validated and cleaned author name
            
        Raises:
            serializers.ValidationError: If the name doesn't meet requirements
        """
        # Strip whitespace and check if empty
        cleaned_name = value.strip()
        
        if not cleaned_name:
            raise serializers.ValidationError("Author name cannot be empty.")
        
        # Check minimum length
        if len(cleaned_name) < 2:
            raise serializers.ValidationError("Author name must be at least 2 characters long.")
        
        # Check that name contains at least one letter
        if not any(char.isalpha() for char in cleaned_name):
            raise serializers.ValidationError("Author name must contain at least one letter.")
        
        return cleaned_name


# Alternative serializer for simpler book representation without nested data
class SimpleBookSerializer(serializers.ModelSerializer):
    """
    Simplified Book serializer without nested author data.
    
    This serializer is useful when you want to serialize books without
    including full author information, preventing potential circular
    references and reducing response size.
    
    Use this when:
    - You need a lightweight book representation
    - You're including books in a list where author details aren't needed
    - You want to avoid deep nesting in API responses
    """
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'author_name']


# Alternative serializer for author without books (lighter weight)
class SimpleAuthorSerializer(serializers.ModelSerializer):
    """
    Simplified Author serializer without nested books.
    
    This serializer provides basic author information without including
    all their books. Useful for:
    - Author listing pages
    - When you need just author references
    - Reducing API response size
    """
    book_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'book_count']
    
    def get_book_count(self, obj):
        """Return the number of books written by this author."""
        return obj.books.count()

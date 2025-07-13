# Create Operation - Book Model

## Creating a Book Instance

### Command:
```python
from bookshelf.models import Book
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
```

### Expected Output:
```python
# The book instance is created and saved to the database
# No output is displayed, but the book is successfully stored with an auto-generated ID
```

### Alternative Creation Method:
```python
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

### Expected Output:
```python
# Returns: <Book: 1984>
# The book instance is created and automatically saved to the database
```

# Retrieve Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

## Expected Output
```python
# The command should retrieve the book and display its attributes:
Title: 1984
Author: George Orwell
Publication Year: 1949
```

## Alternative Commands
```python
# Get all books
all_books = Book.objects.all()
for book in all_books:
    print(book)

# Get book by ID (if you know the ID)
book = Book.objects.get(id=1)
```

## Notes
- The `get()` method retrieves a single object that matches the criteria
- If no object is found, it raises a `DoesNotExist` exception
- If multiple objects match, it raises a `MultipleObjectsReturned` exception 
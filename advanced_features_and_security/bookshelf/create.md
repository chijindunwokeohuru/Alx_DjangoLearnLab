# Create Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

## Expected Output
```python
# The command should execute without errors and return a Book instance
# You can verify the creation by running:
print(book)
# Expected output: "1984 by George Orwell (1949)"
```

## Notes
- This creates a new Book instance in the database
- The `create()` method both creates and saves the object in one step
- The object is automatically assigned an ID and saved to the database 
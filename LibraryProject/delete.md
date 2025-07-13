# Delete Operation - Book Model

## Deleting a Book Instance

### Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
```

### Expected Output
```python
# (1, {'bookshelf.Book': 1})
```

### Verification Command
```python
# Confirm deletion by trying to retrieve all books
all_books = Book.objects.all()
print(all_books)
print(f"Number of books: {all_books.count()}")
```

### Expected Verification Output
```python
# <QuerySet []>
# Number of books: 0
```

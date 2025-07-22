# Delete Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion by trying to retrieve all books
all_books = Book.objects.all()
print(f"Number of books remaining: {all_books.count()}")
for book in all_books:
    print(book)
```

## Expected Output
```python
# The command should delete the book and show no books remain:
Number of books remaining: 0
# (No books will be printed since the list is empty)
```

## Alternative Delete Methods
```python
# Method 1: Delete using the object instance
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Method 2: Delete using QuerySet delete() method
Book.objects.filter(title="Nineteen Eighty-Four").delete()

# Method 3: Delete all books
Book.objects.all().delete()
```

## Notes
- The `delete()` method removes the object from the database permanently
- After deletion, the object no longer exists in the database
- You can verify deletion by checking the count or trying to retrieve the object (which will raise DoesNotExist)
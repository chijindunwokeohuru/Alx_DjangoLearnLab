# Update Operation - Book Model

## Updating a Book Instance

### Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")
```

### Expected Output
```python
# Updated title: Nineteen Eighty-Four
```

### Verification Command
```python
# Verify the update
updated_book = Book.objects.get(author="George Orwell")
print(f"Title: {updated_book.title}")
```

### Expected Verification Output
```python
# Title: Nineteen Eighty-Four
```

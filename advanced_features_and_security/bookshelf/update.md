# Update Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")
```

## Expected Output
```python
# The command should update the book title and display the change:
Updated title: Nineteen Eighty-Four
```

## Alternative Update Methods
```python
# Method 1: Update using the object instance
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Method 2: Update using QuerySet update() method
Book.objects.filter(title="1984").update(title="Nineteen Eighty-Four")

# Verify the update
updated_book = Book.objects.get(title="Nineteen Eighty-Four")
print(updated_book)
```

## Notes
- The `save()` method is required to persist changes to the database
- You can update multiple fields at once
- The `update()` method on QuerySets is more efficient for bulk updates 
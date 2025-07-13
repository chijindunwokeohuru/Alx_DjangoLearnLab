# CRUD Operations - Book Model Documentation

This document contains all the CRUD (Create, Read, Update, Delete) operations performed on the Book model using Django shell.

## Setting up Django Shell

First, open the Django shell:
```bash
python manage.py shell
```

## Import the Book Model

```python
from bookshelf.models import Book
```

## CREATE Operation

### Creating a Book Instance
```python
# Method 1: Create and save separately
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()

# Method 2: Create and save in one step
# book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

**Output:**
```
# No output for method 1 (save operation)
# Method 2 returns: <Book: 1984>
```

## READ Operation

### Retrieving the Book
```python
# Get the specific book
book = Book.objects.get(title="1984")

# Display all attributes
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")

# Alternative: Get all books
all_books = Book.objects.all()
print(all_books)
```

**Output:**
```
Title: 1984
Author: George Orwell
Publication Year: 1949
<QuerySet [<Book: 1984>]>
```

## UPDATE Operation

### Updating the Book Title
```python
# Retrieve the book
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Verify the update
print(f"Updated title: {book.title}")

# Double-check by retrieving again
updated_book = Book.objects.get(author="George Orwell")
print(f"Confirmed title: {updated_book.title}")
```

**Output:**
```
Updated title: Nineteen Eighty-Four
Confirmed title: Nineteen Eighty-Four
```

## DELETE Operation

### Deleting the Book
```python
# Retrieve the book with updated title
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
result = book.delete()
print(result)

# Verify deletion
all_books = Book.objects.all()
print(f"All books after deletion: {all_books}")
print(f"Number of books: {all_books.count()}")
```

**Output:**
```
(1, {'bookshelf.Book': 1})
All books after deletion: <QuerySet []>
Number of books: 0
```

## Summary

All CRUD operations have been successfully performed:
- ✅ **Create**: Book "1984" by George Orwell (1949) was created
- ✅ **Read**: Book details were retrieved and displayed
- ✅ **Update**: Book title was updated from "1984" to "Nineteen Eighty-Four"
- ✅ **Delete**: Book was deleted from the database

The Book model is working correctly with all basic database operations.

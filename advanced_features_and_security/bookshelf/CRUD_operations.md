# CRUD Operations Documentation

This document contains all the CRUD (Create, Read, Update, Delete) operations performed on the Book model in the Django shell.

## Prerequisites
Make sure you have:
1. Created the bookshelf app
2. Defined the Book model with required fields
3. Run migrations (`python manage.py makemigrations bookshelf` and `python manage.py migrate`)
4. Started the Django shell (`python manage.py shell`)

## Complete CRUD Operations Sequence

### 1. CREATE Operation
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
```
**Expected Output:**
```
1984 by George Orwell (1949)
```

### 2. RETRIEVE Operation
```python
# Retrieve the book we just created
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```
**Expected Output:**
```
Title: 1984
Author: George Orwell
Publication Year: 1949
```

### 3. UPDATE Operation
```python
# Update the title of the book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")
```
**Expected Output:**
```
Updated title: Nineteen Eighty-Four
```

### 4. DELETE Operation
```python
# Delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion by checking all books
all_books = Book.objects.all()
print(f"Number of books remaining: {all_books.count()}")
```
**Expected Output:**
```
Number of books remaining: 0
```

## Verification Commands

### Check if migrations are applied
```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookshelf_book';")
tables = cursor.fetchall()
print("Bookshelf_book table exists:", len(tables) > 0)
```

### List all books
```python
from bookshelf.models import Book
books = Book.objects.all()
print(f"Total books: {books.count()}")
for book in books:
    print(book)
```

## Notes
- All operations are performed in the Django shell
- Each operation demonstrates a different aspect of Django's ORM
- The sequence shows the complete lifecycle of a database object
- Error handling is not included for brevity but should be considered in production code 
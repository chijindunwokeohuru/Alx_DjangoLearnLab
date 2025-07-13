# Retrieve Operation - Book Model

## Retrieving a Book Instance

### Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

### Expected Output
```python
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
```

### Alternative Retrieval Methods
```python
# Get all books
all_books = Book.objects.all()
print(all_books)

# Get by ID
book = Book.objects.get(id=1)
print(book)
```

### Expected Output for Alternatives
```python
# <QuerySet [<Book: 1984>]>
# <Book: 1984>
```

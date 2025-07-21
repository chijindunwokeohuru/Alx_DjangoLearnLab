# Django Models - Advanced Relationships

## Project Overview
This project demonstrates the implementation of advanced model relationships in Django, showcasing the use of ForeignKey, ManyToMany, and OneToOne relationships.

## Models Implemented

### 1. Author Model
- **Field**: `name` (CharField)
- **Description**: Represents an author entity

### 2. Book Model
- **Fields**: 
  - `title` (CharField)
  - `author` (ForeignKey to Author)
- **Description**: Represents a book with a relationship to an author (Many-to-One)

### 3. Library Model
- **Fields**:
  - `name` (CharField)
  - `books` (ManyToManyField to Book)
- **Description**: Represents a library that can contain multiple books (Many-to-Many)

### 4. Librarian Model
- **Fields**:
  - `name` (CharField)
  - `library` (OneToOneField to Library)
- **Description**: Represents a librarian associated with exactly one library (One-to-One)

## Relationship Types Demonstrated

### 1. ForeignKey Relationship (One-to-Many)
- **Example**: Book → Author
- **Query**: Find all books by a specific author
- **Implementation**: `Book.objects.filter(author=author)`

### 2. ManyToMany Relationship
- **Example**: Library ↔ Books
- **Query**: List all books in a library
- **Implementation**: `library.books.all()`

### 3. OneToOne Relationship
- **Example**: Librarian → Library
- **Query**: Retrieve the librarian for a library
- **Implementation**: `Librarian.objects.get(library=library)`

## Files Structure

```
django-models/
├── manage.py
├── models.py                    # Main models file (as required)
├── query_samples.py            # Main query samples script (as required)
├── LibraryProject/             # Django project settings
│   ├── settings.py
│   └── ...
└── relationship_app/           # Django app
    ├── models.py              # App-specific models
    ├── query_samples.py       # App-specific query samples
    └── migrations/
        └── 0001_initial.py    # Database migrations
```

## Running the Project

1. **Apply migrations**:
   ```bash
   python manage.py makemigrations relationship_app
   python manage.py migrate
   ```

2. **Run query samples**:
   ```bash
   python query_samples.py
   ```

## Sample Queries Included

The `query_samples.py` script includes:

1. **Query all books by a specific author** (ForeignKey)
2. **List all books in a library** (ManyToMany)
3. **Retrieve the librarian for a library** (OneToOne)

Each query function includes error handling and demonstrates best practices for Django ORM usage.

## Sample Data

The script automatically creates sample data including:
- Authors: J.K. Rowling, George Orwell, Harper Lee
- Books: Harry Potter series, 1984, Animal Farm, To Kill a Mockingbird
- Libraries: Central City Library, Downtown Public Library
- Librarians: Alice Johnson, Bob Smith

This provides a complete working example of advanced Django model relationships.

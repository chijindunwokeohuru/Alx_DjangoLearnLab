from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape
from django.core.exceptions import ValidationError
import re
from .models import Book


def validate_input(value, field_name, max_length=255, pattern=None):
    """
    Validate and sanitize input data to prevent XSS and injection attacks.
    """
    if not value or not value.strip():
        raise ValidationError(f"{field_name} is required and cannot be empty.")
    
    value = value.strip()
    
    if len(value) > max_length:
        raise ValidationError(f"{field_name} cannot exceed {max_length} characters.")
    
    if pattern and not re.match(pattern, value):
        raise ValidationError(f"{field_name} contains invalid characters.")
    
    # Escape HTML to prevent XSS
    return escape(value)


def validate_year(year_str):
    """
    Validate publication year input.
    """
    try:
        year = int(year_str)
        if year < 1000 or year > 2030:
            raise ValidationError("Publication year must be between 1000 and 2030.")
        return year
    except (ValueError, TypeError):
        raise ValidationError("Publication year must be a valid number.")


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """View to display all books - requires can_view permission."""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """View to display a specific book - requires can_view permission."""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


@csrf_protect
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """View to create a new book - requires can_create permission."""
    if request.method == 'POST':
        try:
            # Validate and sanitize input data
            title = validate_input(
                request.POST.get('title'),
                'Title',
                max_length=200,
                pattern=r'^[a-zA-Z0-9\s\-\.\,\:\;\!\?\'\"\(\)]+$'
            )
            author = validate_input(
                request.POST.get('author'),
                'Author',
                max_length=100,
                pattern=r'^[a-zA-Z\s\-\.]+$'
            )
            publication_year = validate_year(request.POST.get('publication_year'))
            
            # Create book using Django ORM (automatically prevents SQL injection)
            Book.objects.create(
                title=title,
                author=author,
                publication_year=publication_year
            )
            messages.success(request, 'Book created successfully!')
            return redirect('book_list')
            
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'An error occurred while creating the book.')
    
    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})


@csrf_protect
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """View to edit an existing book - requires can_edit permission."""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        try:
            # Validate and sanitize input data
            title = validate_input(
                request.POST.get('title'),
                'Title',
                max_length=200,
                pattern=r'^[a-zA-Z0-9\s\-\.\,\:\;\!\?\'\"\(\)]+$'
            )
            author = validate_input(
                request.POST.get('author'),
                'Author',
                max_length=100,
                pattern=r'^[a-zA-Z\s\-\.]+$'
            )
            publication_year = validate_year(request.POST.get('publication_year'))
            
            # Update book using Django ORM (automatically prevents SQL injection)
            book.title = title
            book.author = author
            book.publication_year = publication_year
            book.save()
            
            messages.success(request, 'Book updated successfully!')
            return redirect('book_detail', pk=book.pk)
            
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'An error occurred while updating the book.')
    
    return render(request, 'bookshelf/book_form.html', {
        'book': book,
        'action': 'Edit'
    })


@csrf_protect
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """View to delete a book - requires can_delete permission."""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        try:
            book.delete()
            messages.success(request, 'Book deleted successfully!')
            return redirect('book_list')
        except Exception as e:
            messages.error(request, 'An error occurred while deleting the book.')
            return redirect('book_detail', pk=pk)
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


@login_required
def permission_denied(request):
    """Custom view for permission denied scenarios."""
    return render(request, 'bookshelf/permission_denied.html')

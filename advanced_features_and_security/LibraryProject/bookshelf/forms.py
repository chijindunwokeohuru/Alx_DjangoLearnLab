from django import forms
from django.core.exceptions import ValidationError
from .models import Book


class ExampleForm(forms.ModelForm):
    """
    Example form demonstrating Django form security best practices.
    This form includes input validation, CSRF protection, and secure field handling.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': 200,
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': 100,
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year',
                'min': 1000,
                'max': 2030,
            }),
        }
    
    def clean_title(self):
        """Custom validation for book title."""
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError("Title is required.")
        
        # Remove extra whitespace
        title = title.strip()
        
        # Validate length
        if len(title) < 2:
            raise ValidationError("Title must be at least 2 characters long.")
        
        if len(title) > 200:
            raise ValidationError("Title cannot exceed 200 characters.")
        
        # Check for suspicious patterns that might indicate XSS attempts
        suspicious_patterns = ['<script', 'javascript:', 'onclick=', 'onerror=']
        title_lower = title.lower()
        for pattern in suspicious_patterns:
            if pattern in title_lower:
                raise ValidationError("Title contains invalid characters.")
        
        return title
    
    def clean_author(self):
        """Custom validation for author name."""
        author = self.cleaned_data.get('author')
        if not author:
            raise ValidationError("Author is required.")
        
        # Remove extra whitespace
        author = author.strip()
        
        # Validate length
        if len(author) < 2:
            raise ValidationError("Author name must be at least 2 characters long.")
        
        if len(author) > 100:
            raise ValidationError("Author name cannot exceed 100 characters.")
        
        # Validate that author name contains only letters, spaces, hyphens, and periods
        import re
        if not re.match(r'^[a-zA-Z\s\-\.]+$', author):
            raise ValidationError("Author name can only contain letters, spaces, hyphens, and periods.")
        
        return author
    
    def clean_publication_year(self):
        """Custom validation for publication year."""
        year = self.cleaned_data.get('publication_year')
        
        if year is None:
            raise ValidationError("Publication year is required.")
        
        # Validate year range
        if year < 1000:
            raise ValidationError("Publication year cannot be before 1000.")
        
        if year > 2030:
            raise ValidationError("Publication year cannot be after 2030.")
        
        return year
    
    def clean(self):
        """Additional form-wide validation."""
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        
        # Check for duplicate books
        if title and author:
            existing_book = Book.objects.filter(
                title__iexact=title,
                author__iexact=author
            ).exclude(pk=self.instance.pk if self.instance.pk else None)
            
            if existing_book.exists():
                raise ValidationError("A book with this title and author already exists.")
        
        return cleaned_data


class BookSearchForm(forms.Form):
    """
    Form for searching books with security considerations.
    """
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books...',
        })
    )
    
    search_type = forms.ChoiceField(
        choices=[
            ('all', 'All Fields'),
            ('title', 'Title'),
            ('author', 'Author'),
        ],
        initial='all',
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    
    def clean_query(self):
        """Clean and validate search query."""
        query = self.cleaned_data.get('query')
        
        if query:
            query = query.strip()
            
            # Prevent search queries that are too long
            if len(query) > 200:
                raise ValidationError("Search query cannot exceed 200 characters.")
            
            # Basic XSS prevention
            suspicious_patterns = ['<script', 'javascript:', 'onclick=', 'onerror=']
            query_lower = query.lower()
            for pattern in suspicious_patterns:
                if pattern in query_lower:
                    raise ValidationError("Invalid search query.")
        
        return query

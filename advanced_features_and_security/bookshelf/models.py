from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser model."""
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Create and save a regular user with the given username and password."""
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email) if email else None
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Create and save a superuser with the given username and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser with additional fields."""
    
    date_of_birth = models.DateField(
        null=True, 
        blank=True, 
        help_text="User's date of birth"
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/', 
        null=True, 
        blank=True, 
        help_text="User's profile photo"
    )
    
    objects = CustomUserManager()
    
    def __str__(self):
        """Return string representation of the user."""
        return self.username


class Book(models.Model):
    """A model representing a book in the library."""
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    def __str__(self):
        """Return a string representation of the book."""
        return f"{self.title} by {self.author} ({self.publication_year})"
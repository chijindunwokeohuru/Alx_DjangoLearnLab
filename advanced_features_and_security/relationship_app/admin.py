from django.contrib import admin
from .models import Book, Author, Library, Librarian, UserProfile

# Register other models
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    list_filter = ['author']
    search_fields = ['title', 'author__name']


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    filter_horizontal = ['books']


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ['name', 'library']
    list_filter = ['library']
    search_fields = ['name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']

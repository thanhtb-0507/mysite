from django.contrib import admin

# Require to impliment I18n, also because the "lazy"
from django.utils.translation import gettext_lazy as _

# Register your models here.

from .models import Author, Genre, Book, BookInstance

# Using @admin.register is equivelent of admin.site.register() 
# admin.site.register(Book)
# admin.site.register(...)


# Define the admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = (
		"last_name", 
		"first_name", 
		"date_of_birth", 
		"date_of_death"
	)
	
	fields = [
		"first_name", 
		"last_name", 
		("date_of_birth", "date_of_death")
	]


# Define the inline admin class for BookInstance
class BooksInstanceInline(admin.TabularInline):
	model = BookInstance


# already exist BookAdmin:
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "display_genre")
	
	# new code of 4.4 added here:
	inlines = [BooksInstanceInline]
	

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_filter = ("status", "due_back")

	fieldsets = (
		(None, {
			"fields": ("book", "imprint", "id")}),
		(_("Availability"),{
			"fields": ("status", "due_back")}),
	)

# Define the admin class for Genre
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

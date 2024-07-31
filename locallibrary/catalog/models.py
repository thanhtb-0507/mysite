from django.db import models

# Require to impliment I18n, also because the "lazy"
from django.utils.translation import gettext_lazy as _

# Required for unique book instancesclass
import uuid  

# Used to generate URLs by reversing the URL patternsclass
from django.urls import reverse 



class Genre(models.Model):
	"""Model representing a book genre."""
	name = models.CharField(
		max_length = 200, 
		help_text = _("Enter a book genre (e.g.Science Fiction)"),
		)

	def __str__(self):
		"""String for representing the Model object."""
		return self.name



# Book model
class Book(models.Model):
	"""Model representing a book (but not a specific copy of a book)."""
	title = models.CharField(max_length=200)

	author = models.ForeignKey(
		"Author", 
		on_delete = models.SET_NULL, 
		null = True,
		# provide a human readable name
		verbose_name = _("Author")
		)
	
	summary = models.TextField(
		max_length=1000, 
		help_text = _("Enter a brief description of the book")
		)
	
	isbn = models.CharField(
		'ISBN', 
		max_length = 13, 
		unique = True,
		help_text = _('13 Character <ahref="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
		)
	
	genre = models.ManyToManyField(
		Genre, 
		help_text = _("Select a genre for this book"),
		verbose_name = _("genre"),
		)

	def __str__(self):
		"""String for representing the Model object."""
		return self.title

	def get_absolute_url(self):
		"""Returns the url to access a detail record for this book."""
		return reverse("book-detail", args=[str(self.id)])

	def display_genre(self):
		"""Create a string for the Genre. This is require to display genre in Admin"""
		return ','.join(genre.name for genre in self.genre.all()[:3])



# BookInstance model
class BookInstance(models.Model):
	"""Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
	id = models.UUIDField(
		primary_key = True, 
		default = uuid.uuid4, 
		help_text = _("Unique ID for this particular bookacross whole library")
		)

	book = models.ForeignKey(
		"Book", 
		on_delete = models.RESTRICT,
		verbose_name = _("Book"),
		)
	
	imprint = models.CharField(max_length=200)
	
	due_back = models.DateField(null=True, blank=True)
	
	LOAN_STATUS = (
		('m', _("Maintenance")),
		('o', _("On loan")),
		('a', _("Available")),
		('r', _("Reserved")),
	)

	status = models.CharField(
		max_length = 1,
		choices = LOAN_STATUS,
		blank = True,
		default = 'm',
		help_text = _("Book availability"),
	)

	class Meta:
		ordering = ["due_back"]

	def __str__(self):
		"""String for representing the Model object."""
		return f"{self.id} ({self.book.title})"



# Author model
class Author(models.Model):
	"""Model representing an author."""

	first_name = models.CharField(max_length=100)
	
	last_name = models.CharField(max_length=100)
	
	date_of_birth = models.DateField(null=True, blank=True)
	
	date_of_death = models.DateField("Died", null=True, blank=True)

	class Meta:
		ordering = ["last_name", "first_name"]

	def get_absolute_url(self):
		"""Returns the url to access a particular author instance."""
		return reverse("author-detail", args=[str(self.id)])

	def __str__(self):
		"""String for representing the Model object."""
		return f"{self.last_name}, {self.first_name}"


"""ForeignKey shenanigan:
	Becasue this foreign stuff make data link together so need some
	shenanigan to ensure that the db is not funny up

null = True,
	# null have some relation w/blank, unique
	# here we allow empty value to be store as null

verbose_name = _("Author")
	# provide a human readable name

on_delete = models.<many many cheating>
	# basicly it define the behavior of current or referenced data 
	# when some deletion happen.
	**ASCADE**     : emulate ON DELETE CASCADE, also make obj 
					 containing Fo.Key get reckt
	**PROTECT**    : prevent get reckt, raise ProtectedError
	**RESTRICT**   : raise RestrictedError, only allow deletion 
					 if referenced also get reckt via CASCADE
	**SET_NULL**   : if null == True then Fo.Key = null
	**SET_DEFAULT**: need to set FroreignKey default value before use
	**SET()**      : set ForeignKey as the value that passed 
					 in SET() (variable, funct,…), usually callable 
					 stuff to not invoke querries when import models.py
	**DO_NOTHING** : nop, pass. Cause **IntegrityError** if backend 
					 enforces, have to mannualy add an SQL 
					 **ON DELETE** constraint to the db field
"""


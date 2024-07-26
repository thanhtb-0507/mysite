from django.shortcuts import render
from django.views import generic

# users define
from catalog.models import Book, Author, BookInstance, Genre
from django.shortcuts import get_object_or_404



# Function definition:
def index(request):
	"""View function for home page of site"""
	
	# Generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# Avalable books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact = 'a'). count()
	
	# the 'all()' is implied by default.
	num_authors = Author.objects.count()

	# Number of visits to this view, as counted in the session variable.
	# If no num_visists exsist previously, set it to default '0'
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1
	print(num_visits)
	
	context = {
		"num_books" : num_books,
		"num_instances" : num_instances,
		"num_instances_available" : num_instances_available,
		"num_authors" : num_authors,
		'num_visits': num_visits,
	}
	
	# Render the HTML template index.html with the data in the context variable
	return render(request, "index.html", context = context)


def book_detail_view(request, primary_key):
	"""This function return book else 404 if NomNom."""
	
	# Look up in db for obj of Book model, if no pk then raise 404
	book = get_object_or_404(Book, pk = primary_key)
	
	# invoke render for book detail page
	return render(request, 'catalog/book_detail.html', context={'book': book})


def author_detail_view(request, primary_key):
	"""This function return author else 404 if NULL."""
	
	author = get_object_or_404(Author, pk = primary_key)
	
	return render(request, 'catalog/author_detail.html', context={'author': author})



# Class definition:
class BookListView(generic.ListView):
	"""Class for the view of the book list."""
	model = Book

	# name for the list as a template variable
	context_object_name = "book_list"

	# get the filtered books
	# queryset = Book.objects.filter(title__icontains='war')[:5]

	# specify template name and location
	template_name = 'books/my_arbitrary_template_name_list.html'

	def get_queryset(self):
		# all: return a copy of the current QuerySet
		# filter: returns a new QuerySet fullfil the filter condition
		# select_related: also query author (F_key)
		return Book.objects.select_related("author").all()

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(BookListView, self).get_context_data(**kwargs)
		# Create any data and add it to the context
		context['some_data'] = 'This is just some data'
		return context


class BookDetailView(generic.DetailView):
	model = Book
	paginate_by = 10


class AuthorListView(generic.ListView):
	"""Class for the view of the book list."""
	model = Author

	# name for the list as a template variable
	context_object_name = "author_list"

	# get the filtered author
	# queryset = Author.objects.filter().all()

	# specify template name and location
	template_name = 'authors/my_arbitrary_template_name_list.html'

	def get_queryset(self):
		return Author.objects.all()

	# just a place holder for now
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(AuthorListView, self).get_context_data(**kwargs)
		# Create any data and add it to the context
		context['some_data'] = 'This is just some data'
		return context


class AuthorDetailView(generic.DetailView):
	model = Author
	paginate_by = 10 
	# need to research about .constants 
	# miss the .h, define <> <>, compiler T_T

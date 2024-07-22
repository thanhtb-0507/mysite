from django.shortcuts import render
from django.views import generic

# users define
from catalog.models import Book, Author, BookInstance, Genre
from django.shortcuts import get_object_or_404

from catalog.constants import LOAN_STATUS, ITEMS_PER_PAGE

# Function definition:
def index(request):
    """View function for home page of site"""

    # Generate counts of some of the main objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Avalable books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()

    # the 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        "num_books" : num_books,
        "num_instances" : num_instances,
        "num_instances_available" : num_instances_available,
        "num_authors" : num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context = context)



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


class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = ITEMS_PER_PAGE

    # passing loan_status to view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loan_status'] = dict(LOAN_STATUS)
        return context


class AuthorListView(generic.ListView):
    """Class for the view of the book list."""
    model = Author

    # name for the list as a template variable
    context_object_name = "author_list"


    # specify template name and location
    template_name = 'authors/my_arbitrary_template_name_list.html'

    def get_queryset(self):
        return Author.objects.all()


class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = ITEMS_PER_PAGE
    # need to research about .constants
    # miss the .h, define <> <>, compiler T_T

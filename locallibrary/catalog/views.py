from django.shortcuts import render
from django.views import generic

# users define
# catalog related:
from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm
from .models import Author, Book

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import datetime

from django.views.generic.edit import CreateView, UpdateView, DeleteView


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


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


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

# @login_required
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
	"""Generic class-based view listing books on loan to current user."""
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return (
			BookInstance.objects.filter(borrower=self.request.user)
			.filter(status__exact='o')
			.order_by('due_back')
		)

# also can use staff_member_required, template variable: user.is_staff
# @login_required
# @permission_required('catalog.can_mark_returned', raise_exception=True)
class LibrarianLoanedBooksByUserListView(PermissionRequiredMixin,generic.ListView):
	"""Generic class-based view listing books for librarian."""
	permission_required = ('catalog.can_mark_returned',)
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
	paginate_by = 10

	def get_queryset(self):
		return (
			BookInstance.objects.filter(status__exact='o').order_by('due_back')
		)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )


class BookCreate(PermissionRequiredMixin, CreateView):
	model = Book
	fields = ['title', 'author', 'summary', 'isbn', 'genre']
	initial = {'title': 'New Book'}
	permission_required = 'catalog.add_book'

class BookUpdate(PermissionRequiredMixin, UpdateView):
	model = Book
	fields = ['title', 'author', 'summary', 'isbn', 'genre']
	permission_required = 'catalog.change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
	model = Book
	success_url = reverse_lazy('books')
	permission_required = 'catalog.delete_book'

	def form_valid(self, form):
		try:
			self.object.delete()
			return HttpResponseRedirect(self.success_url)
		except Exception as e:
			return HttpResponseRedirect(
				reverse("book-delete", kwargs={"pk": self.object.pk})
			)

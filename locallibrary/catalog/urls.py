from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "index"),

    # url mapping for book related views
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    
    # url mapping for author related views
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),    
]

# url mapping for loans books
urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LibrarianLoanedBooksByUserListView.as_view(), name='all-borrowed'),
]


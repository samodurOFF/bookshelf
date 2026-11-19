from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('about/', views.about, name='about'),
    path('genres/', views.genre_list, name='genre_list'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/add/', views.author_create, name='author_create'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:pk>/', views.genre_detail, name='genre_detail'),
]

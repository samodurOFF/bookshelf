from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView

from .forms import BookForm, AuthorForm
from .models import Book, Author, Genre

BOOKS = [
    {'id': 1, 'title': 'Мастер и Маргарита', 'author': 'Михаил Булгаков', 'year': 1967, 'rating': 4.8},
    {'id': 2, 'title': 'Преступление и наказание', 'author': 'Фёдор Достоевский', 'year': 1866,
     'rating': 4.6}, {'id': 3, 'title': 'Война и мир', 'author': 'Лев Толстой', 'year': 1869, 'rating': 4.5},
    {'id': 4, 'title': 'Идиот', 'author': 'Фёдор Достоевский', 'year': 1869, 'rating': None},
]

GENRES = ['Роман', 'Классика', 'Приключения']


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Книга «{book.title}» добавлена.')
            return redirect(book)
    else:
        form = BookForm()
    return render(request, 'catalog/book_form.html', {'form': form, 'title': 'Добавить книгу'})


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, 'Изменения сохранены.')
        return redirect(book)
    return render(request, 'catalog/book_form.html', {'form': form, 'title': f'Редактирование: {book.title}'})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Книга «{book.title}» удалена.')
        return redirect('catalog:book_list')
    return render(request, 'catalog/book_confirm_delete.html', {'book': book})


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'catalog/home.html')


def book_list(request):
    author = request.GET.get('author', '').strip()
    books = Book.objects.all()
    if author:
        books = books.filter(author__name=author)
    context = {'books': books, 'title': 'Каталог книг', 'author': author}
    return render(request, 'catalog/book_list.html', context)


def book_detail(request: HttpRequest, pk: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'catalog/book_detail.html', {'book': book})


def about(request):
    technologies = ['Python', 'Django', 'SQLite', 'Git']
    return render(request, 'catalog/about.html', {'technologies': technologies})


def genre_list(request):
    return render(request, 'catalog/genre_list.html', {'genres': Genre.objects.all()})


def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    return render(request, 'catalog/genre_detail.html', {'genre': genre, 'books': genre.books.all()})


def author_list(request):
    return render(request, 'catalog/author_list.html', {'authors': Author.objects.all()})


class BookListView(ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    context_object_name = 'books'
    extra_context = {'title': 'Каталог книг'}


class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'catalog/author_detail.html', {'author': author, 'books': author.books.all()})


def author_create(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        author = form.save()
        messages.success(request, f'Автор «{author.name}» добавлен.')
        return redirect(author)
    return render(request, 'catalog/book_form.html', {'form': form, 'title': 'Добавить автора'})

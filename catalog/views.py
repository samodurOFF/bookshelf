from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView
from django.db.models import Count, Sum, Avg, Max, Min
from .forms import BookForm, AuthorForm
from .models import Book, Author, Genre


def can_manage(user, book):
    return user.is_authenticated and (user.is_staff or book.created_by_id == user.id)

def with_annotate(queryset):
    return queryset.annotate(books_count=Count('books'))

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            form.save_m2m()
            messages.success(request, f'Книга «{book.title}» добавлена.')
            return redirect(book)
    else:
        form = BookForm()
    return render(request, 'catalog/book_form.html', {'form': form, 'title': 'Добавить книгу'})


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not can_manage(request.user, book):
        raise PermissionDenied
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, 'Изменения сохранены.')
        return redirect(book)
    return render(request, 'catalog/book_form.html', {'form': form, 'title': f'Редактирование: {book.title}'})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not can_manage(request.user, book):
        raise PermissionDenied
    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Книга «{book.title}» удалена.')
        return redirect('catalog:book_list')
    return render(request, 'catalog/book_confirm_delete.html', {'book': book})


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'catalog/home.html')


def book_list(request):
    q = request.GET.get('q', '').strip()
    genre_id = request.GET.get('genre', '').strip()
    author = request.GET.get('author', '').strip()
    books = Book.objects.all()
    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__name__icontains=q))
    if genre_id.isdigit():
        books = books.filter(genre__id=int(genre_id))


    if author:
        books = books.filter(author__name=author)
    viewed = request.session.get('recent_books', [])
    books_viewed = Book.objects.filter(pk__in=viewed)
    context = {
        'books': books,
        'title': 'Каталог книг',
        'genres': Genre.objects.all(),
        'q': q,
        'author': author,
        'recent_books': books_viewed
    }
    return render(request, 'catalog/book_list.html', context)


def book_detail(request: HttpRequest, pk: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=pk)
    viewed = request.session.get('recent_books', [])
    if book.pk in viewed:
        viewed.remove(book.pk)
    viewed.insert(0, book.pk)
    request.session['recent_books'] = viewed[:5]
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
    authors = with_annotate(Author.objects.all())
    return render(request, 'catalog/author_list.html', {'authors': authors})


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

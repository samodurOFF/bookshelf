from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404

BOOKS = [
    {'id': 1, 'title': 'Мастер и Маргарита', 'author': 'Михаил Булгаков', 'year': 1967, 'rating': 4.8},
    {'id': 2, 'title': 'Преступление и наказание', 'author': 'Фёдор Достоевский', 'year': 1866,
     'rating': 4.6}, {'id': 3, 'title': 'Война и мир', 'author': 'Лев Толстой', 'year': 1869, 'rating': 4.5},
    {'id': 4, 'title': 'Идиот', 'author': 'Фёдор Достоевский', 'year': 1869, 'rating': None},
]

GENRES = ['Роман', 'Классика', 'Приключения']


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'catalog/home.html')


def book_list(request):
    author = request.GET.get('author', '').strip()
    books = BOOKS
    if author:
        books = [book for book in BOOKS if book['author'] == author]
    context = {'books': books, 'title': 'Каталог книг', 'author': author}
    return render(request, 'catalog/book_list.html', context)


def book_detail(request: HttpRequest, pk: int) -> HttpResponse:
    for book in BOOKS:
        if book['id'] == pk:
            return render(request, 'catalog/book_detail.html', {'book': book})

    raise Http404('Книга не найдена')


def about(request):
    technologies = ['Python', 'Django', 'SQLite', 'Git']
    return render(request, 'catalog/about.html', {'technologies': technologies})


def genre_list(request):
    return render(request, 'catalog/genre_list.html', {'genres': GENRES})

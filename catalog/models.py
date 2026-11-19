from django.db import models
from django.conf import settings
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField('название', max_length=100, unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:genre_detail', kwargs={'pk': self.pk})


class Author(models.Model):
    name = models.CharField('имя', max_length=100)
    bio = models.TextField('биография', blank=True)

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:author_detail', kwargs={'pk': self.pk})


class Book(models.Model):
    title = models.CharField('название', max_length=255)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='books')
    genre = models.ManyToManyField(Genre, verbose_name='жанры', related_name='books', blank=True)
    description = models.TextField('описание', blank=True)
    year = models.PositiveSmallIntegerField('год издания')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='добавил', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='books_added')

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:book_detail', kwargs={'pk': self.pk})

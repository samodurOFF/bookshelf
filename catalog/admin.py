from django.contrib import admin
from django.contrib.admin import register

from .models import *

admin.site.register(Genre)
admin.site.register(Author)


@register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'created_by')
    list_filter = ('year', 'genre')
    search_fields = ('title', 'author__name')

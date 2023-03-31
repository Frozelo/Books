from django.contrib import admin

from .models import Books, UserBookRelation

admin.site.register(Books)

admin.site.register(UserBookRelation)
from django.db import models


class Author(models.Model):
    author_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.author_name}'

from django.contrib.auth.models import User
from django.db import models

import authors.models


class Books(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author = models.CharField(max_length=255, default='')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="my_book")
    readers = models.ManyToManyField(User, through="UserBookRelation", related_name="books")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)  # Кеширующее поле

    def __str__(self):
        return f'{self.id}: {self.name}, {self.author}'


class UserBookRelation(models.Model):
    RATE_CHOICES = ((1, "Ok"),
                    (2, "Good"),
                    (3, "Amazing"),
                    (4, "Incredible"),
                    (5, "Awesome")
                    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveIntegerField(choices=RATE_CHOICES, null=True)



    def __str__(self):
        return f'{self.user.username}, {self.book.name}'


    # To do - не считать рейтинг книги, если пользователь, который ставит оценку уже оценивал эту книгу ранее

    def save(self, *args, **kwargs):
        from orders.logic import set_rating

        creating = not self.pk

        old_rating = self.rate
        super().save(*args, **kwargs)
        new_rating = self.rate
        if (old_rating != new_rating) or creating:
            set_rating(self.book)

from django.contrib.auth.models import User
from django.test import TestCase

from orders.logic import set_rating, set_rating_test, set_rating_test2
from orders.models import Books, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1", first_name="User1", last_name="123")
        self.user2 = User.objects.create(username="user2", first_name="User2", last_name="123")
        self.user3 = User.objects.create(username="user3", first_name="User3", last_name="123")
        self.book_1 = Books.objects.create(name='Test book 1', price=1000.00,
                                           author='Author 1', owner=self.user1)
        # self.book_2 = Books.objects.create(name='Test book 2', price=999.00,
        #                                    author='Author 5', owner=self.user1)
        # self.book_3 = Books.objects.create(name='Test book Author 1', price=950.00,
        #                                    author='Author 2', owner=self.user2)
        UserBookRelation.objects.create(user=self.user1, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book_1, like=True, rate=4)
        UserBookRelation.objects.create(user=self.user3, book=self.book_1, like=True, rate=5)

    def test_ok(self):
        print(set_rating(self.book_1))




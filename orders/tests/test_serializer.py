from django.contrib.auth.models import User
from django.db.models import Count, Case, When
from django.test import TestCase

from orders.models import Books, UserBookRelation

# Тест должен содержать проверку на полноценность полей сериализатора BookSerializer.
# То есть условно бдует expection data, которая будеи состоять из списка с book_1  и book_2, а также current data,
# которая будет создаваться с помощью нашего сериализатора
# Создадим book_1 и book_2
from orders.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1", first_name="User1", last_name="123")
        self.user2 = User.objects.create(username="user2", first_name="User2", last_name="123")
        self.user3 = User.objects.create(username="user3", first_name="User3", last_name="123")
        self.book_1 = Books.objects.create(name='Test book 1', price=1000.00,
                                           author='Author 1', owner=self.user1)
        self.book_2 = Books.objects.create(name='Test book 2', price=999.00,
                                           author='Author 5', owner=self.user1)
        # self.book_3 = Books.objects.create(name='Test book Author 1', price=950.00,
        #                                    author='Author 2', owner=self.user2)

    def test_good(self):
        UserBookRelation.objects.create(user=self.user1, book=self.book_1, like=True)
        UserBookRelation.objects.create(user=self.user2, book=self.book_1, like=True)
        UserBookRelation.objects.create(user=self.user3, book=self.book_1, like=True)

        UserBookRelation.objects.create(user=self.user1, book=self.book_2, like=True)
        UserBookRelation.objects.create(user=self.user2, book=self.book_2, like=True)
        UserBookRelation.objects.create(user=self.user3, book=self.book_2, like=True)
        books = Books.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('id')

        data = BookSerializer(books, many=True).data
        expection_data = [
            {
                'id': self.book_1.id,
                'name': 'Test book 1',
                'price': '1000.00',
                "author": 'Author 1',
                "owner_name": self.user1.username,
                "readers": [
                    {
                        "first_name": 'User1',
                        'last_name': "123"
                    },
                    {
                        "first_name": 'User2',
                        'last_name': "123"
                    },
                    {
                        "first_name": 'User3',
                        'last_name': "123"
                    }

                ],
                "annotated_likes": 3
            },
            {
                'id': self.book_2.id,
                'name': 'Test book 2',
                'price': '999.00',
                "author": 'Author 5',
                "owner_name": self.user1.username,
                "readers": [
                    {
                        "first_name": 'User1',
                        'last_name': "123"
                    },
                    {
                        "first_name": 'User2',
                        'last_name': "123"
                    },
                    {
                        "first_name": 'User3',
                        'last_name': "123"
                    }

                ],
                "annotated_likes": 3
            }

        ]
        # current_data = BookSerializer([self.book_1, self.book_2], many=True).data

        print(expection_data, data)
        self.assertEqual(expection_data, data)


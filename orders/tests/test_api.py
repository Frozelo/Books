import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from orders.models import Books, UserBookRelation
from orders.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.staff = User.objects.create(username='test_staff', is_staff=True)
        self.book_1 = Books.objects.create(name='Test book 1', price=1000.00,
                                           author='Author 1', owner=self.user)
        self.book_2 = Books.objects.create(name='Test book 2', price=999.00,
                                           author='Author 5', owner=self.user)
        self.book_3 = Books.objects.create(name='Test book Author 1', price=950.00,
                                           author='Author 2', owner=self.user)

    def test_get(self):
        url = reverse('books-list')  # !!!!!!!!!!!используется название класса модели
        response = self.client.get(url)
        print(response)
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)  # many - для того, чтобы был сериализатор для book_1 и book_2

    def test_get_search(self):
        url = reverse('books-list')
        response = self.client.get(url,
                                   data={'search': 'Author 1'})
        serializer_data = BookSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        print(response.data)

    def test_get_ordering(self):
        url = reverse('books-list')
        response = self.client.get(url,
                                   data={'ordering': 'price'})
        serializer_data = BookSerializer([self.book_3, self.book_2, self.book_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        print(response.data)

    def test_get_minus_ordering(self):
        url = reverse('books-list')
        response = self.client.get(url,
                                   data={'ordering': '-price'})
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        url = reverse('books-list')
        self.client.force_login(self.user)
        data = {"name": "Programming in Python3",
                "price": "1500.00",
                "author": "Test_Author",
                }
        json_data = json.dumps(data)
        response = self.client.post(url, json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        print(Books.objects.last().owner)

    def test_put(self):
        url = reverse('books-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        data = {
            "name": self.book_1.name,
            "price": 1500.00,

        }
        json_data = json.dumps(data)
        response = self.client.put(url, json_data, content_type='application/json')
        print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete(self):
        url = reverse('books-detail', args=(self.book_2.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url, self.book_2.id, content_type='application/json')
        print(response.data)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_put_notOwner(self):
        url = reverse('books-detail', args=(self.book_1.id,))
        self.client.force_login(self.user2)
        data = {
            "name": self.book_1.name,
            "price": 1500.00,

        }
        json_data = json.dumps(data)
        response = self.client.put(url, json_data, content_type='application/json')
        print(response.data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_notOwner(self):
        url = reverse('books-detail', args=(self.book_2.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url, self.book_2.id, content_type='application/json')
        print(response.data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_put_is_staff(self):
        url = reverse('books-detail', args=(self.book_1.id,))
        self.client.force_login(self.staff)
        data = {
            "name": self.book_1.name,
            "price": 1500.00,

        }
        json_data = json.dumps(data)
        response = self.client.put(url, json_data, content_type='application/json')
        print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_is_staff(self):
        url = reverse('books-detail', args=(self.book_2.id,))
        self.client.force_login(self.staff)
        response = self.client.delete(url, self.book_2.id, content_type='application/json')
        print(response.data)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


class UserBookRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.staff = User.objects.create(username='test_staff', is_staff=True)
        self.book = Books.objects.create(name='Test book 1', price=1000.00,
                                           author='Author 1', owner=self.user)
        self.book_2 = Books.objects.create(name='Test book 2', price=999.00,
                                           author='Author 5', owner=self.user)
        self.book_355 = Books.objects.create(name='Test book Author 1', price=950.00,
                                           author='Author 2', owner=self.user)
        self.books = Books.objects.all()

    def test_patch_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_355.id,))  # !!!!!!!!!!!используется название класса модели
        # Он принимает тройку, как айди (то есть видит айдишник), но говорит, что должен быть соответствие с моделью Books. Думаю, что проблема в
        # полях.............................................................................................................................................

        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        relation = UserBookRelation.objects.get(user = self.user, book = self.book_355.id)
        self.assertTrue(relation.like)

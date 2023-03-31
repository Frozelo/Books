from django.db.models import Avg

from orders.models import UserBookRelation


def set_rating_test(book):
    book_rating = UserBookRelation.objects.filter(book=book).aggregate(rating=Avg('userbookrelation__rate'))
    return book_rating


"""
НЕПРАВИЛЬНЫЙ СПОСОБ
Так как  мы обращаемся непосредственно к модели UserBookRelation, то смысла rating=Avg('userbookrelation__rate') нет, т.к мы и так в этой модели
=> нужно работать напрямую и писать rating=Avg('rate')
"""


def set_rating_test2(self):
    return UserBookRelation.objects.filter(book=self.id).aggregate(rating=Avg('rate'))


"""
Тестовая функция, которую написал сам. Вроде работает :)
"""


def set_rating(book):
    book_rating = UserBookRelation.objects.filter(book=book).aggregate(rating=Avg('rate')).get('rating')
    book.rating = book_rating
    book.save()

"""
Работаю с этой функцией. Вообще aggregate выводит словарь, поэтому с помощью get достанем значение у ключа rating
"""

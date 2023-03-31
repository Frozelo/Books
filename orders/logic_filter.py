from django_filters import rest_framework as filters

from orders.models import Books


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BookFilter(filters.FilterSet):
    price = filters.RangeFilter()
    author = filters.Filter(lookup_expr='icontains')

    class Meta:
        model = Books
        fields = ['price', 'author']



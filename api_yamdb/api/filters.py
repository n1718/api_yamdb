from django_filters import rest_framework as filters

from review.models import Title


class TitleFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')

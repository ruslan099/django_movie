from django import template
from movies.models import *

register = template.Library()

@register.simple_tag()
def get_categories():
    """Вывод категорий"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies():
    """Получение последних фильмов"""
    movies = Movie.objects.order_by('id')[:5]
    return {'last_movies': movies}
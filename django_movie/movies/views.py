from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.db.models import Q

from .forms import *
from .models import *


class GenreYear:
    """Жанры и года фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'
    # def get(self, request):
    #     movies = Movie.objects.all()
    #     return render(request, 'movies/movies.html', {'movie_list': movies})


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'
    template_name = 'movies/movie_detail.html'
    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     return render(request, 'movies/movie_detail.html', {'movie': movie})



class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(f'/review/{pk}')


class ActorView(GenreYear, DetailView):
    """Вывод информации об актёре"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMovieView(GenreYear, ListView):
    """Фильтров фильмов"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) | 
            Q(genres__in=self.request.GET.getlist('genre'))
        )
        return queryset
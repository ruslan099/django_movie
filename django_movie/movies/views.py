from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from flask import template_rendered

from .forms import *
from .models import *


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'
    # def get(self, request):
    #     movies = Movie.objects.all()
    #     return render(request, 'movies/movies.html', {'movie_list': movies})


class MovieDetailView(DetailView):
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


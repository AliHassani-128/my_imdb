from django.urls import path
from film.api.views import FilmView, RateFilm, SearchFilm

urlpatterns = [
    path('list-films/', FilmView.as_view(), name='list-films'),
    path('rate-film/',RateFilm.as_view(),name='rate-film'),
    path('search/',SearchFilm.as_view(),name='search')
]

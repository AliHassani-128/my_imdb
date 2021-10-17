from itertools import chain

from django.db.models import Q
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from film.api.serializers import FilmSerializer, FilmRateSerializer, SearchSerializer
from film.models import Film, Film_Rate_User


class FilmView(generics.ListAPIView):
    queryset = Film.objects.all().order_by('pub_date')
    serializer_class = FilmSerializer


class RateFilm(generics.CreateAPIView):
    model = Film_Rate_User
    serializer_class = FilmRateSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.get_serializer()
        return Response(serializer.data)

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Your vote has been saved'})
        else:
            return Response(serializer.errors)


class SearchFilm(generics.ListAPIView):
    search_fields = ['name','director','description']
    filter_backends = (filters.SearchFilter,)
    queryset = Film.objects.all()
    serializer_class = FilmSerializer













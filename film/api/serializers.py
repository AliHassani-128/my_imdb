from rest_framework import serializers

from film.models import Film, Film_Rate_User


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        depth = 1
        fields = ['name', 'director', 'pub_date', 'description', 'mean_rate', 'file']


class FilmRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film_Rate_User
        fields = '__all__'

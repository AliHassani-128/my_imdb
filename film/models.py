from django.db import models

# Create your models here.
from user.models import CustomUser


class Film(models.Model):
    name = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now=True)
    description = models.TextField()
    file = models.FileField(upload_to='films')

    @property
    def mean_rate(self):
        mean = 0
        films = Film_Rate_User.objects.filter(film__name=self.name)
        for film in films:
            mean += film.rate
        if len(films) > 0:
            return mean / len(films)
        else:
            return 0


class Film_Rate_User(models.Model):
    film =  models.ForeignKey(Film,on_delete=models.CASCADE,related_name='rate_film')
    rate = models.IntegerField(default=0)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    comment = models.TextField()






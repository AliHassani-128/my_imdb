from django.contrib import admin

# Register your models here.
from film.models import Film, Film_Rate_User

admin.site.register(Film)
admin.site.register(Film_Rate_User)

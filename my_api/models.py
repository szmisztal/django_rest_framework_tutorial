from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@receiver(post_save, sender = User)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)

class ExtraInfo(models.Model):
    GENRES = {
        (0, 'Unknown'),
        (1, 'Horror'),
        (2, 'Sci-Fi'),
        (3, 'Drama'),
        (4, 'Comedy')
    }

    time = models.IntegerField()
    genre = models.IntegerField(choices = GENRES, default = 0)

class Movie(models.Model):
    title = models.CharField(max_length = 32)
    description = models.TextField(max_length = 256)
    after_premiere = models.BooleanField(default = False)
    premiere = models.DateField(null = True, blank = True)
    pub_year = models.IntegerField()
    imdb_rating = models.DecimalField(max_digits = 4, decimal_places= 2, null = True, blank = True)

    extra_info = models.OneToOneField(ExtraInfo, on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self):
        return self.name()

    def name(self):
        return f"{self.title} ({self.pub_year})"

class Review(models.Model):
    description = models.TextField(max_length = 256, default = '')
    stars = models.IntegerField(default = 0)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE, related_name = 'reviews')

class Actor(models.Model):
    name = models.CharField(max_length = 32)
    surname = models.CharField(max_length = 32)
    movies = models.ManyToManyField(Movie)

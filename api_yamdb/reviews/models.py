from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Titles(models.Model):
    name = models.TextField(max_length=100)
    birth_year = models.IntegerField()
    description = models.TextField(max_length=200, null=True, blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

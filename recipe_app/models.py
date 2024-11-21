from django.db import models
# from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.models import User


class Chef(models.Model):
    # user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    # bio = models.TextField()
    #
    # def __str__(self):
    #     return self.user.email

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)  # Chef's name, optional
    bio = models.TextField(blank=True, null=True)  # Chef's bio, optional text field

    def __str__(self):
        return self.name if self.name else self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    categories = models.ManyToManyField(Category)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.title


class Post(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post for {self.recipe.title}"

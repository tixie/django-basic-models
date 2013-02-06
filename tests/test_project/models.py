
from django.db import models
import basic_models


class Category(basic_models.DefaultModel):
    name = models.CharField(max_length=1024)
    pass


class Post(basic_models.SlugModel):
    category = models.ForeignKey(Category)
    body = models.TextField()

class Comment(basic_models.SlugModel):
    post = models.ForeignKey(Post)
    body = models.TextField()

class Homepage(basic_models.OnlyOneActiveModel):
    hero = models.TextField()
    posts = models.ManyToManyField(Post, blank=True)
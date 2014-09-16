from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

class Blog(models.Model):
    caption = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category)

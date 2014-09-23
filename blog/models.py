from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.caption


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __unicode__(self):
        return self.username




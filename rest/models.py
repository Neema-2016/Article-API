from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from cloudinary.models import CloudinaryField


# Create your models here.
class Article(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    email = models.EmailField()
    date= models.DateTimeField(auto_now_add=True)
    # image=models.FileField(max_length=None, allow_empty_file=False)
    # image = models.FileField(blank=True)

    def __str__(self):
         return str(self.title)


# Since django can't store multiple images in one field, this model will store all images and a FK to create a rshp
class ArticleImage(models.Model):
    # user = get_object_or_404(User, pk)
    article = models.ForeignKey(Article, default=None, on_delete=models.CASCADE)
    # images = models.ImageField(upload_to='images')
    image = CloudinaryField('image')

    def __str__(self):
        return str(self.article.title)
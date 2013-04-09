from django.db import models
from django.contrib.auth.models import User

class Content(models.Model):
	image = models.ImageField(upload_to='content',null=True,blank=True)
	description = models.CharField(max_length=1000)
	

class Playlist(models.Model):
	name = models.CharField(max_length=100)
	content = models.ManyToManyField(Content)
	metric = models.IntegerField()
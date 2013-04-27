from django.db import models
from django.contrib.auth.models import User

class Content(models.Model):
	image = models.FileField(upload_to='static/content',null=True,blank=True)
	description = models.CharField(max_length=1000,null=True,blank=True)
	uploaded_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	metric = models.IntegerField(default=12)
	is_video = models.BooleanField()
	def __unicode__(self):
		return str(self.image)

class Playlist(models.Model):
	name = models.CharField(max_length=100)
	content = models.ManyToManyField(Content,null=True,blank=True)
	metric = models.IntegerField(null=True,blank=True)
	auto_all = models.BooleanField()
	def __unicode__(self):
		return self.name
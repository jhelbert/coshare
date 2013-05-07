from django.db import models
from django.contrib.auth.models import User

class Content(models.Model):
	image = models.FileField(upload_to='static/content',null=True,blank=True)
	description = models.CharField(max_length=1000,null=True,blank=True)
	uploaded_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	favorited_time = models.DateTimeField(blank=True,null=True)
	metric = models.IntegerField(default=12)
	is_video = models.BooleanField()
	owner = models.ForeignKey('UserProfile',null=True,blank=True)
	def __unicode__(self):
		return str(self.image)
	

class Album(models.Model):
	name = models.CharField(max_length=100)
	content = models.ManyToManyField(Content,null=True,blank=True)
	auto_all = models.BooleanField()
	owner = models.ForeignKey(User,null=True,blank=True)
	def __unicode__(self):
		return self.name


class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	queue = models.ForeignKey(Album)

	def __unicode__(self):
		return self.user.username

class Child(models.Model):
	name = models.CharField(max_length=100)
	album = models.ForeignKey(Album)

class Couple(models.Model):
	members = models.ManyToManyField(UserProfile)
	albums = models.ManyToManyField(Album)
	children = models.ManyToManyField(Child,null=True,blank=True)


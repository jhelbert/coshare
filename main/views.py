from main.models import Content,Playlist
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext

def main(request):
	playlists = Playlist.objects.all()
	return render_to_response('index.html', 
		{
		 "playlists":playlists
		},
		context_instance=RequestContext(request))# Create your views here.

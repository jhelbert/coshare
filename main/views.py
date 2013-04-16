from main.models import Content,Playlist
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect

def mosaic(request):
	query_all_playlist()
	return render_to_response('mosaic.html', 
		{
		},
		context_instance=RequestContext(request))# Create your views here.



def main(request):
	playlists = Playlist.objects.all()
	query_all_playlist()
	return render_to_response('index.html', 
		{
		 "playlists":playlists
		},
		context_instance=RequestContext(request))# Create your views here.

def query_all_playlist():
	all_playlist = Playlist.objects.get(auto_all=True)
	all_content = Content.objects.all()
	for content in all_content:
		all_playlist.content.add(content)

@csrf_exempt
def upload(request):

	for uploaded_content in request.FILES.getlist('content'):
		print uploaded_content
		new_content = Content()
		file_content = ContentFile(uploaded_content.read()) 
		new_content.image.save(uploaded_content.name, file_content)
	return HttpResponseRedirect('/')


@csrf_exempt
def add(request):
	content =  request.GET.getlist('eles')
	content = tuple(content)
	album = Playlist.objects.get(id=request.GET.get('album'))
	for c in content:
		print "C:%s" % c
		album.content.add(Content.objects.get(id=c))
	return HttpResponseRedirect('/')

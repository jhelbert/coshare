from main.models import Content,Playlist
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
import json
import datetime

def mosaic(request):
	query_all_playlist()
	get_recently_added()
	return render_to_response('mosaic.html', 
		{
		},
		context_instance=RequestContext(request))# Create your views here.


def home(request):
	return render_to_response('landing_page.html', 
		{
		},
		context_instance=RequestContext(request))# Create your views here.

def get_recently_added():
	recently_added_plist = Playlist.objects.get(name="Recently Added")
	print "got ra plist"
	recently_added_plist.content.clear()
	content = Content.objects.all()
	for c in content:
		if c.uploaded_date:
			if c.uploaded_date + datetime.timedelta(days=2) > datetime.datetime.today():
				recently_added_plist.content.add(c)
	print "done with get recently added"
@csrf_exempt
def new_plist(request):
	name = request.POST.get('name')
	plist = Playlist(name=name)
	plist.save()
	return HttpResponseRedirect('/')
def main(request):
	get_recently_added()
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


@csrf_exempt
def open_modal(request):
	imageID = request.POST.get('id')
	imageID = str(imageID)
	all_content = Content.objects.all()
	res = {}
	res["des"] = ""
	for content in all_content:
		if imageID == str(content.id):
			res["des"] = content.description
			return HttpResponse(json.dumps(res),content_type="application/json")

	return HttpResponse(json.dumps(res),content_type="application/json")
			
	


@csrf_exempt
def change_description(request):
	imageID = request.POST.get('id')
	imageID = str(imageID)
	newDes = request.POST.get('description')
	for content in Content.objects.all():
		if imageID == str(content.id):
			content.description = str(newDes)
			content.save()
	return HttpResponse("done")


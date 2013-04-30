from main.models import Content,Album
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from random import randint
import json
import datetime
import random

def main(request):
	query_all_album()
	get_recently_added()

	try:
		recent_plist = Album.objects.get(name="Recently Added")
		recently_added = recent_plist.content.all()
		recently_added_1 = recently_added[:4]
		recently_added_2 = recently_added[4:8]
	except:
		recently_added_1 = None
		recently_added_2 = None
	try:
		fav_plist = Album.objects.get(name="Recently Favorited")
		favs = fav_plist.content.all()
		fav_1 = favs[:4]
		fav_2 = favs[4:8]
	except:
		fav_1 = None
		fav_2 = None

	return render_to_response('index.html', 
		{
			"recently_added_1":recently_added_1,
			"recently_added_2":recently_added_2,
			"favs_1":fav_1,
			"favs_2": fav_2
		},
		context_instance=RequestContext(request))# Create your views here.

def get_recently_added():
	try:
		recently_added_plist = Album.objects.get(name="Recently Added")
		print "got ra plist"
		recently_added_plist.content.clear()
		content = Content.objects.all()
		for c in content:
			if c.uploaded_date:
				if c.uploaded_date + datetime.timedelta(days=2) > datetime.datetime.today():
					recently_added_plist.content.add(c)
		print "done with get recently added"
	except:
		pass

def mobile(request):
	return render_to_response('mobile.html', 
		{

		},
		context_instance=RequestContext(request))# Create your views here.

@csrf_exempt
def new_plist(request):
	name = request.POST.get('name')
	plist = Album(name=name)
	plist.save()
	return HttpResponseRedirect('/')

def browse(request):
	get_recently_added()
	albums = Album.objects.all()
	query_all_album()
	return render_to_response('browse.html', 
		{
		 "albums":albums
		},
		context_instance=RequestContext(request))# Create your views here.

def query_all_album():
	try:
		all_album = Album.objects.get(auto_all=True)
		all_content = Content.objects.all()
		for content in all_content:
			all_album.content.add(content)
	except:
		pass

@csrf_exempt
def upload(request):
	album_id = request.POST.get('album')
	
	album = None
	if album_id != -1 and album_id != None:
		print album_id
		try:
			album = Album.objects.get(id=album_id)
		except:
			album = None

	for uploaded_content in request.FILES.getlist('content'):
		print uploaded_content
		new_content = Content()
		file_content = ContentFile(uploaded_content.read()) 
		new_content.image.save(uploaded_content.name, file_content)
		ext = uploaded_content.name[uploaded_content.name.find('.')+1:]
		if ext not in ["jpg",'jpeg','png','gif']:
			new_content.is_video = True
		new_content.metric = int(random.random() * 6) + 8
		new_content.save()
		new_content.save()
		if album:
			album.content.add(new_content)
			album.save()
	return HttpResponseRedirect('/browse/')

@csrf_exempt
def add_album(request):
	name = request.POST.get('name')
	print name
	new_album = Album(name=name)
	new_album.save()
	return HttpResponse('OK')

@csrf_exempt
def add_content(request):
	album_id = request.POST.get('album_id')
	pic_id = request.POST.get('pic_id')
	album = Album.objects.get(id=int(album_id))
	print 'got plist'
	content = Content.objects.get(id=int(pic_id))
	if album.name == "Favorites":
		content.metric = 20
		content.save()
	print 'got content'
	album.content.add(content)
	album.save()

	return HttpResponse('OK')

@csrf_exempt
def remove_content(request):
	album_id = request.POST.get('album_id')
	pic_id = request.POST.get('id')
	album = Album.objects.get(id=int(album_id))
	print 'got plist'
	content = Content.objects.get(id=int(pic_id))
	if album.name == "Favorites":
		content.metric = int(random.random() * 6) + 8
		content.save()
	print 'got content'
	album.content.remove(content)
	album.save()
	return HttpResponse('OK')

@csrf_exempt
def add(request):
	content =  request.GET.getlist('eles')
	content = tuple(content)
	album = Album.objects.get(id=request.GET.get('album'))
	for c in content:
		print "C:%s" % c
		album.content.add(Content.objects.get(id=c))
	return HttpResponseRedirect('/')


@csrf_exempt
def open_modal(request):
	imageID = request.POST.get('id')
	imageID = str(imageID)
	print imageID
	all_content = Content.objects.all()
	res = {}
	res["des"] = ""
	photos = {}
	albumList = []

	all_album = Album.objects.all()
		
	for plist in all_album:
		for content in plist.content.all():
			if str(content.id) == imageID:
				albumList.append(plist.name)
				c = plist.content.all()
				max_num = min(3,len(c))
				photos[plist.name] = []
				# Get randon three photos from list
				if len(c) > 3: 
					count = 0
					index_set = []
					while count < max_num:
						index = randint(0,len(c)-1);
						if index in index_set:
							continue
						index_set.append(index)
						photos[plist.name].append(c[index].image.url)
						count += 1
				else:
					for i in range(0,max_num):
						photos[plist.name].append(c[i].image.url)
				break

	res["albums"] = albumList
	res["photos"] = photos

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
	return HttpResponse("error")


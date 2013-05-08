from main.models import Content,Album, UserProfile, Couple, Child
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from random import randint
import json
from django.contrib.auth import authenticate,login, logout
import datetime
import random
import os
from django.contrib.auth.models import User

def login_page(request):
	return render_to_response('login.html', 
		{
		},
		context_instance=RequestContext(request))

def get_user(request):
	userprof = None
	if not request.user.is_anonymous():
		userprof = User.objects.get(username=request.user.username)
	return userprof

def get_user_profile(request):
	userprof = None
	print request.user
	try:
		userprof = UserProfile.objects.get(user=request.user)
	except:
		pass
		
	return userprof

def get_couple(userprof):

	return Couple.objects.get(members=userprof)


def go_to_recently_added(request):
	userprof = get_user_profile(request)
	couple = get_couple(userprof)
	possible_albums = couple.albums.all()
	recently_added_plist = possible_albums.get(name="Recently Added")
	return HttpResponseRedirect('/browse/?id=' + str(recently_added_plist.id))

def go_to_recently_favorited(request):
	userprof = get_user_profile(request)
	couple = get_couple(userprof)
	possible_albums = couple.albums.all()
	recently_added_plist = possible_albums.get(name="Recently Favorited")
	return HttpResponseRedirect('/browse/?id=' + str(recently_added_plist.id))
@csrf_exempt
def login_user(request):
	email = request.POST.get('email')
	password = request.POST.get('password')
	user = User.objects.get(email=email)

	if user.check_password(password):
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request,user)
		userprof = get_user_profile(request)
		if userprof is None:
			print "no userprof"
			if user.first_name:
				queue = Album(name=user.first_name + "'s Queue")
			else:
				queue = Album(name=user.username + "'s Queue")
			queue.save()
			userprof = UserProfile(user=user,queue=queue)
			userprof.save()


		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/login/')

@csrf_exempt
def logout_user(request):
	logout(request)

	return HttpResponseRedirect('/login/')

def main(request):
	user = get_user(request)
	
	
	userprof = get_user_profile(request)

	if userprof is None:
		return HttpResponseRedirect('/login/')
	couple = get_couple(userprof)
	children = couple.children.all();
	get_recently_added(couple)
	get_recently_favorited(couple)
	query_all_album(couple)
	name = ""
	if user:
		name = user.first_name + " " + user.last_name

	try:
		possible_albums = couple.albums.all()
		recent_plist = possible_albums.get(name="Recently Added")
		recently_added = recent_plist.content.all()
		recently_added_1 = recently_added[:4]
		recently_added_2 = recently_added[4:8]
	except:
		recently_added_1 = None
		recently_added_2 = None
	try:
		possible_albums = couple.albums.all()
		fav_plist = possible_albums.get(name="Recently Favorited")
		favs = fav_plist.content.all()
		fav_1 = favs[:4]
		fav_2 = favs[4:8]
	except:
		fav_1 = None
		fav_2 = None

	# ignore shit above, below is what counts

	albums = [couple.albums.get(name=x) for x in ("All Content",
										     "Recently Added",
										     "Recently Favorited")]

	albums = [album for album in albums if len(album.content.all()) > 0]

	queue_size = len(userprof.queue.content.all())

	return render_to_response('index.html', 
		{
			"recently_added_1":recently_added_1,
			"recently_added_2":recently_added_2,
			"favs_1":fav_1,
			"favs_2": fav_2,
			"userprof":userprof,
			"name":name,
			"children":children,
			"albums": albums,
			"queue_size": queue_size,
		},
		context_instance=RequestContext(request))# Create your views here.

def get_recently_added(couple):
	try:
		possible_albums = couple.albums.all()
		recently_added_plist = possible_albums.get(name="Recently Added")
		print "got ra plist"
		recently_added_plist.content.clear()
		content = query_all_album(couple).content.all()
		for c in content:
			if c.uploaded_date:
				if c.uploaded_date + datetime.timedelta(days=2) > datetime.datetime.today():
					recently_added_plist.content.add(c)
		print "done with get recently added"
	except:
		print "recently added failed"

def get_recently_favorited(couple):
	try:
		possible_albums = couple.albums.all()
		favorited = possible_albums.get(name="Favorites")
		recently_added_plist = possible_albums.get(name="Recently Favorited")
		print "got ra plist"
		recently_added_plist.content.clear()
		content = query_all_album(couple).content.all()
		for c in content:
			if c.favorited_time:
				if c.favorited_time + datetime.timedelta(days=1) > datetime.datetime.today():
					for f in favorited.content.all():
						if f.id == c.id:
							recently_added_plist.content.add(c)
		print "done with get recently added"
	except:
		pass


def mobile(request):
	user_albums = []
	all_albums = Album.objects.all()
	for album in all_albums:
		if album.name not in ["Recently Favorited", "Recently Added", "All Added", "All Favorites", "Favorites", "All Content", "Tasks"] and "Queue" not in album.name:
			user_albums.append(album)
	print user_albums
	return render_to_response('mobile.html', 
		{
			"albums":user_albums
		},
		context_instance=RequestContext(request))# Create your views here.

@csrf_exempt
def new_plist(request):
	print "new_plist"
	userprof = get_user_profile(request)
	print userprof
	couple = get_couple(userprof)
	print "got couple"
	name = request.POST.get('name')
	plist = Album(name=name)
	plist.save()
	if couple:
		couple.albums.add(plist)
		couple.save()
	else:
		return HttpResponse("create a couple")
	return HttpResponseRedirect('/')

def browse(request):
	user = get_user(request)
	name = None
	if user:
		name = user.first_name + " " + user.last_name

	userprof = get_user_profile(request)

	if userprof == None:
	 	return HttpResponseRedirect('/login/')

	couple = get_couple(userprof)
	children = couple.children.all()
	get_recently_added(couple)
	get_recently_favorited(couple)
	print "got couple"
	albums = couple.albums.all()
	query_all_album(couple)
	album_id = request.GET.get('id')
	selected_album = None
	try:
		selected_album = Album.objects.get(id=album_id)
		print selected_album
	except:
		pass
	print children
	print albums

	return render_to_response('browse.html', 
		{
		 "albums":albums,
		 "selected_album": selected_album,
		 "user_queue_id": userprof.queue.id,
		 "children":children,
		 "userprof":user,
		 "name":name
		},
		context_instance=RequestContext(request))# Create your views here.

def query_all_album(couple):
	possible_albums = couple.albums.all()
	all_album = possible_albums.get(auto_all=True)
	all_album.content.clear()
	all_content = Content.objects.all()
	for content in all_content:
		for userprof in couple.members.all():
			if userprof == content.owner:
				print content
				all_album.content.add(content)

	all_album.save()
	return all_album


@csrf_exempt
def upload(request):
	mobile = request.POST.get('mobile')
	album_id = request.POST.get('album')
	userprof = get_user_profile(request)
	try:
		delete = request.POST.get('deleted').split('|')
	except:
		delete = []
	album = None
	if album_id != -1 and album_id != None:
		print album_id
		try:
			album = Album.objects.get(id=album_id)
		except:
			album = None
	new_album_name = request.POST.get('new_album_name')
	if new_album_name:
		
		couple = get_couple(userprof)
		album = Album(name=new_album_name)
		album.save()
		couple.albums.add(album)
		couple.save()
	index = 0
	for uploaded_content in request.FILES.getlist('content'):
		if str(index) not in delete:
			print uploaded_content
			new_content = Content()
			new_content.owner = userprof
			file_content = ContentFile(uploaded_content.read()) 
			new_content.image.save(uploaded_content.name, file_content)
			# ext = uploaded_content.name[uploaded_content.name.find('.')+1:]
			ext = os.path.splitext(uploaded_content.name)[1]
			if ext in ["mov","MOV","mp4"]:
				new_content.is_video = True
			new_content.metric = int(random.random() * 6) + 8
			new_content.save()
			new_content.save()
			if album:
				album.content.add(new_content)
				album.save()
			if mobile:
				userprof.queue.content.add(new_content);
				userprof.queue.save()
		else:
			print "not uploading index:%i" % index
		index += 1

	return HttpResponseRedirect('/browse/')

@csrf_exempt
def add_album(request):
	userprof = get_user_profile(request)
	couple = get_couple(userprof)
	name = request.POST.get('name')
	plist = Album(name=name)
	plist.save()
	if couple:
		couple.albums.add(plist)
		couple.save()
	else:
		return HttpResponse("create a couple")
	return HttpResponse('%i' % (plist.id, ))

@csrf_exempt
def rename_album(request):
	new_name = request.POST.get("name")
	album_id = request.POST.get("album_id")
	album = Album.objects.get(id=album_id)
	album.name = new_name
	album.save()
	return HttpResponse('ok')

@csrf_exempt
def remove_album(request):
	album_id = request.POST.get('album_id')
	album = Album.objects.get(id=int(album_id))
	album.delete()
	return HttpResponse('ok')

@csrf_exempt
def add_content(request):
	album_id = request.POST.get('album_id')
	pic_id = request.POST.get('pic_id')
	print "pic_id:%s" % pic_id
	album = Album.objects.get(id=int(album_id))
	print 'got plist'
	content = Content.objects.get(id=int(pic_id))
	print "got content"
	if album.name == "Favorites":
		content.metric = 20
		content.save()
	print 'got content'
	album.content.add(content)
	album.save()
	print album.content.all()

	if album.name == "Favorites":
		content.favorited_time = datetime.datetime.now()
		content.save()

	return HttpResponse("%i" % (len(album.content.all()), ))

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
	userprof = get_user_profile(request)
	couple = get_couple(userprof)
	for a in couple.albums.all():
		a.content.remove(content)
		a.save()
	return HttpResponse("%i" % (len(album.content.all()), ))

@csrf_exempt
def delete_content(request):
	pic_id = request.POST.get('id')
	content = Content.objects.get(id=int(pic_id))
	content.owner = None
	content.save()
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
						index = randint(0,len(c)-1)
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


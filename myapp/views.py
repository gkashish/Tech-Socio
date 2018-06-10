from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from .models import Profile,Post,Comment,like,dislike
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from .serializers import PostSerializer
# Create your views here.

def re(request):
	return redirect("/home/")

@login_required(login_url='/login/')
def home(request,**kwargs):
	if kwargs:
		if User.objects.filter(username = kwargs['username']).exists():
			user = User.objects.get(username = kwargs['username'])
		else:
			return HttpResponse("No user exist with this username.")
	else:
		user = request.user
	top_posts = Post.objects.filter(user = user)
	top_posts = top_posts[:30]
	string = "welcome "+request.user.username
	return render(request,"home.html",{"user":user,"post":top_posts,"Message":string})

@login_required(login_url='/login/')
def Like(request):
	if(request.method == "POST"):
		id = request.POST["post_id"]
		username = request.POST["user"]
		post = Post.objects.get(id = id)
		if Post.like_set.get(user = user).exists():
			return JsonResponse(status=500,data={"Message":"Already Liked"})
		user = User.objects.get(username = username)
		liker = like()
		if(post.Likes == 0):
			post.Likes = 1
		else:
			post.Likes += 1
		liker.user = user
		liker.liked_to = post
		post.save()
		liker.save()
		return JsonResponse({"count":post.Likes})

@login_required(login_url='/login/')
def Dislike(request):
	if(request.method == "POST"):
		id = request.POST["post_id"]
		username = request.POST["user"]
		post = Post.objects.get(id = id);
		user = User.objects.get(username = username)
		if Post.dislike_set.get(user = user).exists():
			return JsonResponse(status=500,data={"Message":"Already Liked"})
		disliker = dislike()
		if(post.Dislikes == 0):
			post.Dislikes = 1
		else:
			post.Dislikes += 1
		disliker.user = user
		disliker.disliked_to = post
		post.save()
		disliker.save()
		return JsonResponse({"count":post.Dislikes})



@login_required(login_url='/login/')
def post(request):
	new_post = Post()
	new_post.user = request.user
	new_post.description = request.POST.get('description',None)
	new_post.image = request.FILES.get('image',None)
	new_post.save()
	print(new_post)
	serializer = PostSerializer(new_post)
	return HttpResponseRedirect('/home/')


def login1(request):
	user = User()
	next_url = request.GET.get("next",'/home/')
	if request.user.is_authenticated:
		return HttpResponseRedirect(next_url)
	if request.method == "POST":
		next_Url = request.POST.get("next",'')
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username,password = password)
		if user is not None:
			auth_login(request,user)
			return JsonResponse(status = 200, data = {"Message" : next_url})
		else:
			return JsonResponse(status= 404,data= {'Message': "Incorrect Username/Password."})
	return render(request,"login.html",{})



def register(request):
	next_Url = request.GET.get("next",'/home/')
	if request.user.is_authenticated:
		return HttpResponseRedirect(next_Url)
	if request.method == 'POST':
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		email = request.POST.get('email', None)
		first_name = request.POST.get('first', None)
		last_name = request.POST.get('last', None)
		if User.objects.filter(email = email).exists():
			return JsonResponse(status= 404,data={"Message": "Email is already registered"})	
		if(User.objects.filter(username = username).exists()):
			return JsonResponse(status= 404,data={"Message":"Username already exists."})
		user, created = User.objects.get_or_create(username=username, email=email , first_name = first_name, last_name = last_name)
		if created:
		    user.set_password(password) 
		    user.save()
		    return JsonResponse(status = 200, data = {"Message" : next_Url})
		else :
			return JsonResponse(status= 404,data={"Message":"Internal Server Error."})
	return render(request,'register.html',{})

def logout_(request):
	logout(request)
	return HttpResponseRedirect('/home/')
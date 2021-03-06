from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Profile(models.Model):
	#dp = models.ImageField(default="https://ssl.gstatic.com/accounts/ui/avatar_2x.png")
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	def __str__(self):
		return self.userName

class Post(models.Model):
	URL = models.CharField(max_length=1000,blank = True)
	image = models.FileField(blank=True)
	description = models.CharField(max_length=100000, default="",blank=True)
	Likes = models.IntegerField(default=0)
	Dislikes = models.IntegerField(default=0)
	created_at = models.DateTimeField(default = datetime.now)
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	def __str__(self):
		return str(self.id)
	class meta:
		ordering = ['-id']

class Comment(models.Model):
	comment_description = models.CharField(max_length=100000, blank = False)
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	posted_on = models.ForeignKey(Post,on_delete=models.CASCADE)
	class meta:
		order_by = ['id']
	def __str__(self):
		return 'Commented by' + self.user.username

class like(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	liked_to = models.ForeignKey(Post,on_delete=models.CASCADE)
	def __str__(self):
		return self.user.username

class dislike(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	disliked_to = models.ForeignKey(Post,on_delete=models.CASCADE)
	def __str__(self):
		return self.user.username


from django.conf import settings
from django.db import models
from .validators import validate_content
from django.urls import reverse
import datetime
from django.utils import timezone
# Create your models here.
# ORM - Object Relational Mapper
# models are classes represent database table,
# each attribute of the class represt a table
# every model is a table of a database, every instance represnt columns of that table 

class TweetManager(models.Manager):
	def retweet(self,user,parent_obj):
		if parent_obj.parent:
			og_parent = parent_obj.parent
		else:
			og_parent = parent_obj
		qs = self.get_queryset().filter(
			user = user,parent=og_parent).filter(
			timestamp__year=timezone.now().year,
			timestamp__month=timezone.now().month,
			timestamp__day=timezone.now().day,
			)

		# qs = self.get_queryset().filter(user = user,parent=parent_obj)

		if qs.exists():
			return None

		obj = self.model(
			parent = og_parent,
			user = user,
			content = parent_obj.content,
			)
		obj.save()
		return obj


class Tweet(models.Model):
	parent = models.ForeignKey("self",blank=True,null=True) # give retweet credit to the parents tweet
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	content = models.CharField(max_length=240,validators = [validate_content]) # tweet box length
	updated = models.DateTimeField(auto_now=True) # if update tweet
	timestamp = models.DateTimeField(auto_now_add=True) # timezone now

	objects = TweetManager()

	def __str__(self):
		return str(self.content)

	def get_absolute_url(self): #django method
		return reverse("tweet:detail" , kwargs={"pk":self.pk}) # show the url after create a post

	class Meta:
		ordering = ['-timestamp']  # rever the tweet order, show most recent


	"""
	Basic content verified code
	"""
	# def clean_content(self,*args,**kwargs):
	# 	content = self.cleaned_data.get("content")
	# 	if content == " ":
	# 		raise forms.ValidationError("Can't be a blank space")
	# 	return content
	
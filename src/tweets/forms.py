from django import forms
from .models import Tweet

class TweetModelForm(forms.ModelForm):
	content = forms.CharField(label='',widget=forms.Textarea(attrs={
		"placeholder":"Share your feelings",
		"class":"form-control"
		})) # tweet create textarea setting
 	# class Meta:
		# model = Tweet
		# fields = [
		# 	#"user", # not defined user
		# 	"content"
		# ]
	class Meta:
		model = Tweet
		fields = ["content"]
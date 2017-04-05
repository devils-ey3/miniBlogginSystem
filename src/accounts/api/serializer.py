from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.urls import reverse_lazy



User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
	followers_count = serializers.SerializerMethodField()
	url = serializers.SerializerMethodField()
	class Meta:
		"""
		THis is the publicly display user serializers
		"""
		model = User
		fields = [
			'username',
            'first_name',
            'last_name',
            'followers_count',
            'url'
			#'email',
			#'facebook_profile_link'
		]

	def get_followers_count(self,obj): # here obj contains the fields
		return 0

	def get_url(self,obj):
		return reverse_lazy("profiles:detail",kwargs={"username":obj.username})
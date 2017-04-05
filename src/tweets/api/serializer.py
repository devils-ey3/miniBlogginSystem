from django.utils.timesince import timesince
from rest_framework import serializers
from accounts.api.serializer import UserDisplaySerializer
from tweets.models import Tweet

class ParentTweetModelSerializer(serializers.ModelSerializer):
	user = UserDisplaySerializer(read_only=True) # Generally it is write only mode (POST method), the read_only mode is send request as GET method
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()

	class Meta:
		model = Tweet

		fields = [
			'id',
			'user', # now the user override the list content with <user = UserDisplaySerializer()> this statement
			'content',
			'timestamp', #from newsest post first and oldest post last
			'date_display',
			'timesince',
		]

	def get_is_retweet(self,obj): # for preventing retweet of retwwet post
		if obj.parent:
			return True
		return False

	def get_date_display(self,obj):
		return obj.timestamp.strftime("%d-%b-%Y, at %I:%M %p")

	def get_timesince(self,obj):
		return timesince(obj.timestamp) + " ago"

class TweetModelSerializer(serializers.ModelSerializer):
	user = UserDisplaySerializer(read_only=True) # Generally it is write only mode (POST method), the read_only mode is send request as GET method
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()
	parent = ParentTweetModelSerializer(read_only=True)



	class Meta:
		model = Tweet

		fields = [
			'id',
			'user', # now the user override the list content with <user = UserDisplaySerializer()> this statement
			'content',
			'timestamp', #from newsest post first and oldest post last
			'date_display',
			'timesince',
			'parent'
		]


	def get_date_display(self,obj):
		return obj.timestamp.strftime("%d-%b-%Y, at %I:%M %p")

	def get_timesince(self,obj):
		return timesince(obj.timestamp) + " ago"
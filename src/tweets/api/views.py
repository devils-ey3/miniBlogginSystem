from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .pagination import StandardResultsSetPagination
from .serializer import TweetModelSerializer
from tweets.models import Tweet
from django.db.models import Q


class TweetCreateAPIView(generics.CreateAPIView):
	serializer_class = TweetModelSerializer
	permissions_classes = [permissions.IsAuthenticated]


	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class LikeToggleAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request, pk, format=None):
		tweet_qs = Tweet.objects.filter(pk=pk)
		message = "Not allowed"
		if request.user.is_authenticated():
			is_liked = Tweet.objects.like_toggle(request.user, tweet_qs.first())
			return Response({'liked': is_liked})
		return Response({"message": message}, status=400)

class TweetListAPIView(generics.ListAPIView):
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultsSetPagination

	def get_serializer_context(self):
		try :
			context = super(TweetListAPIView, self).get_serializer_context(*args, **kwargs)
		except:
			context = super(TweetListAPIView, self).get_serializer_context()
		context['request'] = self.request
		return context

	def get_queryset(self, *args, **kwargs):
		requested_user = self.kwargs.get("username")
		
		if requested_user:
			qs = Tweet.objects.filter(user__username=requested_user).order_by("-timestamp")
		else:
			im_following = self.request.user.profile.get_following() # none
			qs1 = Tweet.objects.filter(user__in=im_following)
			qs2 = Tweet.objects.filter(user=self.request.user)
			qs = (qs1 | qs2).distinct().order_by("-timestamp")
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter( #making queryies q
					Q(content__icontains=query) | # search by contant
					Q(user__username__icontains=query) #search by user and username
					)
		return qs	



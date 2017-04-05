from django.conf.urls import url
from .views import  TweetListAPIView,TweetCreateAPIView
#from .views import tweet_detail_view,tweet_list_view
#from django.views.generic.base import RedirectView

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    # url(r'^$', RedirectView.as_view(url="/")), # redirect to home
    url(r'^$', TweetListAPIView.as_view(),name='list'), # /api/tweet/
    url(r'^create/$', TweetCreateAPIView.as_view(),name='create'), # /api/tweet/create
    # url(r'^(?P<pk>\d+)/$', TweetDetailView.as_view(),name='detail'), # /tweet/1/ work tweet_deatils_view function work in views.py
    # url(r'^(?P<pk>\d+)/update/$', TweetUpdateView.as_view(),name='update'), #/tweet/1/update
    # url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(),name='delete'), #/tweet/1/delete

]
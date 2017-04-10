from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .models import Tweet
from django.db.models import Q
from django.views import View
from django.http import HttpResponseRedirect

# Create your views here.

# Create view

class RetweetView(View):
	def get(self,request, pk,*args,**kwargs):
		tweet = get_object_or_404(Tweet, pk=pk)
		if request.user.is_authenticated():
			new_tweet = Tweet.objects.retweet(request.user,tweet)		
			return HttpResponseRedirect("/")
		return HttpResponseRedirect(tweet)

class TweetCreateView(FormUserNeededMixin,CreateView): #LoginRequiredMixin
	# queryset = Tweet.objects.all()
	# form = TweetModelForm
	form_class = TweetModelForm
	template_name = "tweets/create_view.html" 
	# redirect to models.py 

	#success_url = "/tweet/create/"
	#success_url = reverse_lazy("tweet:detail")
	
	#login_url = '/admin/' # redirect unauthorized user to login page

	# def form_valid(self,form):
	# 	if self.request.user.is_authenticate():
	# 		form.instance.user = self.request.user
	# 		return super(TweetCreateView.self).form_valid(form)
	# 	else:
	# 		form._error[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in to continue"])
	# 		return self.form_invalid(form)
# """ Function base view """
# def tweet_create_view(request):
# 	form = TweetModelForm(request.POST or None)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.user = request.user
# 		instance.save()
# 	context = {
# 		"form":form
# 	}
# 	return render(request,'tweets/create_view.html',context)
#####################################################################

# update view
class TweetUpdateView(LoginRequiredMixin,UserOwnerMixin,UpdateView):
	queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = "tweets/update_view.html"
	#success_url = "/tweet/"	
	#login_url = '/admin/'

# query into database
class TweetDetailView(DetailView):
	#template_name = "tweets/detail_view.html"
	queryset = Tweet.objects.all()
	# def get_object(self):
	# 	pk = self.kwargs.get('pk')
	# 	print(pk)
	# 	return Tweet.objects.get(id=pk)
class TweetDeleteView(LoginRequiredMixin,DeleteView):
	model = Tweet
	template_name = "tweets/delete_confirm.html"
	success_url = reverse_lazy("tweet:list")

class TweetListView(LoginRequiredMixin,ListView):
	#template_name = "tweets/list_view.html" # template_name variable name is fixed
	# If you want ot ignore template_name then create same html file into app name template folder

	#searching function
	def get_queryset(self,*args,**kwargs):
		qs = Tweet.objects.all()
		query = self.request.GET.get("q",None)
		if query is not None:
			qs = qs.filter( #making queryies q
			Q(content__icontains=query) | # search by contant
			Q(user__username__icontains=query) #search by user and username
				) 
		return qs

	def get_context_data(self,*args,**kwargs):
		context = super(TweetListView,self).get_context_data(*args,**kwargs)
		context['create_form'] = TweetModelForm() # create_form connected with POST button
		#context['create_url'] = reverse_lazy("tweets:create")
		context['create_url'] = reverse_lazy("tweet:create")

		return context

# <-- Same as upper class function -->
def tweet_detail_view(request,pk=None): # here pk = id
	# obj = Tweet.objects.get(pk=pk) # GET from database
	# print('obj -->',obj)
	obj = get_object_or_404(Tweet,pk=pk)
	context = {
	"object" : obj
	}
	return render(request,"tweets/detail_view.html",context)

# def tweet_list_view(request):
# 	queryset = Tweet.objects.all() # GET a list of item
# 	# queryset is object model itself,
# 	# object model is user,content, update etc in tweet class
# 	for x in queryset:
# 		print(x.content)
# 	context = {
# 	"object_list" : queryset
# 	}
# 	return render(request,"tweets/list_view.html",context)


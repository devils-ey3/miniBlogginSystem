from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseRedirect
from .models import UserProfile
from django.views.generic.edit import FormView
# Create your views here.
from .forms import UserRegisterForm


User = get_user_model()

class UserRegisterView(FormView):
	template_name = 'accounts/user_register_form.html'
	form_class = UserRegisterForm
	success_url = '/login'

	def form_valid(self, form):
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		new_user = User.objects.create(username=username, email=email)
		new_user.set_password(password)
		new_user.save()
		return super(UserRegisterView, self).form_valid(form)

class UserDetailsView(DetailView):
	template_name = "accounts/user_detail.html"
	queryset = User.objects.all()

	def get_object(self):
		"""
		This function does make url with username, like profiles/misa/,, generally the function come with primary key but when you try to show the link with profile name then it is horrible,,coppied from stackoverflow. Django didn't change the method of DeatilsView, slug_field change is also not working here
		The username is same as urls.py
		"""
		return get_object_or_404(User,username__iexact=self.kwargs.get("username"))

	def get_context_data(self,*args,**kwargs):
		context = super(UserDetailsView,self).get_context_data(*args,**kwargs)
		following = UserProfile.objects.is_following(self.request.user,self.get_object())
		context['following'] = following
		return context

class UserFollowView(View):
	def get(self, request, username, *args, **kwargs):
		toggle_user = get_object_or_404(User,username__iexact=username)
		if request.user.is_authenticated():
			is_following = UserProfile.objects.toggle_follow(request.user,toggle_user)
		return redirect("profiles:detail", username=username)



		# if we user HttpResponseRedirect then it would be like 
		# url = reverse ("profiles:detail", kwargs={"username":username})
		# HttpResponseRedirect(url)
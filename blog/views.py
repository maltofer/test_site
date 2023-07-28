from typing import Any, Dict, Optional
from django.db.models import Q
from django.db import models
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Profile, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegitserForm, EditProfileForm, PostForm, EditCommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserChangeForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.decorators import method_decorator


# def home(request):
#     context = {}
#     return render(request, 'blog/home.html', context)
@login_required(login_url='login')
def home(request):
    return render(request, 'blog/home.html',)

@method_decorator(login_required(login_url='login'), name='dispatch')
class PostView(ListView):
    model = Post
    template_name = 'blog/post.html'
    ordering = ['id']

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            queryset = Post.objects.filter(Q(title__icontains=query))
        else:
            queryset = Post.objects.all()
        return queryset
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class ArticleDetail(DetailView):
    model = Post
    template_name = 'blog/articles_details.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        post = self.object  # Access the current post object through self.object
        total_likes = post.total_likes()
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class AddPostView(CreateView):
    model = Post
    template_name = 'blog/post-form.html'
    form_class = PostForm  # Use the custom form here
    enctype = "multipart/form-data"  # You can set enctype here

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Post created successfully!')
        return response



def register(request):
    if request.user.is_authenticated:
        return redirect ("home")
    else:
        form = UserRegitserForm()
        if request.method == "POST":
            form = UserRegitserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                messages.success(request, f"The account has been created for {username}",)
                return redirect("login")
            else:
                messages.info(request, 'Opps! Something went wrong, please check username or password')
        context = {'form':form,}    
        return render(request, 'blog/register.html', context)      

def login_user(request):
    if request.user.is_authenticated:
        return redirect ("home")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                return redirect("home")
            else:
                messages.info(request, "Username or Password is not correct")
        return render(request, 'blog/login.html')


def log_out(request):
    logout(request)
    return redirect("login")

@login_required(login_url='login')
def Like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))

@method_decorator(login_required(login_url='login'), name='dispatch')
class UserEditView(LoginRequiredMixin, generic.UpdateView):
    form_class = EditProfileForm
    template_name = "blog/edit_profile.html"
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        # Save the user model
        user = form.save()

        return super().form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')    
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'blog/user_profile.html'

    def get_context_data(self, *args,**kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args,**kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        posts = Post.objects.filter(author=page_user.user)
        context['posts'] = posts
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditPofilePage(generic.UpdateView):
    model = Profile
    template_name = 'blog/update_user_profile.html'
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'pintrest_url', 'location', 'education']
    success_url = reverse_lazy('home')


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = EditCommentForm

    def get_success_url(self):
        return reverse_lazy("article-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        # Set the post for the comment
        form.instance.post_id = self.kwargs['pk']
        
        # Set the author for the comment (logged-in user)
        form.instance.author = self.request.user
        
        response = super().form_valid(form)
        messages.success(self.request, 'Comment added successfully!')
        return 
    

def contact_us(request):
    if request.method == 'POST':
        # Process the form data here (sending emails, etc.)
        # Example: Get the data submitted via the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Send email to your Gmail account
        send_mail(
            subject=f'From AcadmiaPost from {name}',
            message=f'From: {name} ({email})\n\nMessage: {message}',
            from_email='dragon169590@gmail.com',
            recipient_list=['dragon169590@gmail.com'],
            fail_silently=False,
        )

        # Redirect to a thank-you page after form submission (optional)
        return render(request, 'blog/thank_you.html', {'name': name})

    return render(request, 'blog/contact.html')

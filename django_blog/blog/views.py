from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in user after registration
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')  # redirect to home or blog list page
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

# Profile view
@login_required
def profile_view(request):
    return render(request, 'blog/profile.html')
#--------------------------------------------------------------------------------------------------------
# List all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # template to render
    context_object_name = 'posts'
    ordering = ['-published_date']  # newest first
    

# Show post details
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# Create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user  # set logged-in user as author
        return super().form_valid(form)

# Update a post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # only author can update

# Delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')  # redirect after deletion

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
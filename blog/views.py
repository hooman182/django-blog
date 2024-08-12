from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage

# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'posts.html'

def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, status = Post.Status.PUBLISHED, publish__year=year, publish__month=month, publish__day=day, slug=post_slug)
    
    return render(request, 'postDetail.html', {'post': post})

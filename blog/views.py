from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect, render
from blog.forms import CommentForm
from blog.models import Comment, Post
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_POST
# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'posts.html'

def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, status = Post.Status.PUBLISHED, publish__year=year, publish__month=month, publish__day=day, slug=post_slug)
    
    comments = Comment.objects.filter(active=True, post=post.id)
    form = CommentForm()
    
    return render(request, 'postDetail.html', {'post': post, 'comments':comments, 'form':form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        
    return render(request, 'comment.html', {'post': post, 'comment':comment})
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from blog.models import Post

# Create your views here.
def post_list(request):
    posts = Post.published.all()
    return render(request, 'posts.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status = Post.Status.PUBLISHED)
    return render(request, 'postDetail.html', {'post': post})
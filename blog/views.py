from django.shortcuts import get_object_or_404, render
from blog.forms import CommentForm
from blog.models import Comment, Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

# Create your views here.    
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag_list = Tag.objects.all()
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    return render(request, 'posts.html', {'posts': posts, 'tags':tag_list, 'tag': tag})

def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, status = Post.Status.PUBLISHED, publish__year=year, publish__month=month, publish__day=day, slug=post_slug)
    
    comments = Comment.objects.filter(active=True, post=post.id)
    form = CommentForm()
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) 
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', 'publish')[:4]

    return render(request, 'postDetail.html', {'post': post, 'comments':comments, 'form':form, 'similar_posts':similar_posts})


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
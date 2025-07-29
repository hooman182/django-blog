from django.shortcuts import render
from blog.models import Post


def index(request):
    posts = Post.objects.all()
    context = {"articles": posts}
    return render(request, "home/index.html", {"articles": posts})

def about(request):
    return render(request, "/about/about.html")

def skills(request):
    return render(request, "skills/skills.html")

def experiences(request):
    return render(request, "experiences/experiences.html")
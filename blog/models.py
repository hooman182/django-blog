from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250, unique_for_date="publish", allow_unicode=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = CKEditor5Field("Content", config_name="extends", blank=True, null=True)
    image = models.ImageField(
        upload_to="cover_images/", default=None, blank=True, null=True
    )
    publish = models.DateTimeField(timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    objects = models.Manager()
    published = PublishManager()
    tags = TaggableManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [models.Index(fields=["-publish"])]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )

    def read_time(self):
        from html import unescape
        from django.utils.html import strip_tags

        string = self.body + unescape(strip_tags(self.body))
        total_words = len((string).split())

        words_per_minute = 200
        read_time_minutes = round(total_words / words_per_minute)
        return max(1, read_time_minutes)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = CKEditor5Field(config_name="default")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [models.Index(fields=["created"])]

    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"

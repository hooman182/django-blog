from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<str:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<str:post_slug>',
         views.post_detail, name='post_detail'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment')
]

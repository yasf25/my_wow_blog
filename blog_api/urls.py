from django.urls import path, re_path
from .views import PostList, UserPostList

urlpatterns = [
    path("<int:pk>/", UserPostList.as_view(), name="post_detail"),
    path("", PostList.as_view(), name="post_list"),
    re_path('^user/(?P<id>.+)/$', UserPostList.as_view()), # new
]
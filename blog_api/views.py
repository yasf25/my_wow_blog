from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from blog.models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly

from rest_framework import generics


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get(self, request, format = None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPostList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    def get_queryset(self):
        user = self.kwargs['id']
        return Post.objects.filter(author=user)



    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post,
                                    data=request.data,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
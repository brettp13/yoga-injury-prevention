from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, BlogPost
from .serializers import AuthorSerializer, BlogPostSerializer


class ListSelectAuthors(APIView):
    """
    List authors or select a single author.
    """
    def get(self, request):
        """
        List authors.
        """
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Select a single author
        """
        try:
            author_id = request.data['author_id']
            author = Author.objects.get(id=author_id)
            serializer = AuthorSerializer(author)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'author_id missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class ListSelectBlogPosts(APIView):
    """
    List all blog posts or select a specific one.
    """
    def get(self, request):
        """
        List blog posts.
        """
        blog_posts = BlogPost.objects.all().order_by('-created')
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            blog_post_id = request.data['blog_post_id']
            blog_post = BlogPost.objects.get(id=blog_post_id)
            serializer = BlogPostSerializer(blog_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'blog_post_id missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

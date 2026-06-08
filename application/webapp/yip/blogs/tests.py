import json

from rest_framework import status
from rest_framework.test import APITestCase

from testing_utils import utils

from .models import Author, BlogPost


class ListSelectAuthors(APITestCase):
    def setUp(self):
        self.list_authors_url = '/blog/list-authors/'
        self.select_author_url = '/blog/select-author/'
        self.test_author = Author.objects.create(first_name='John', last_name='Doe')

    def test_listing_authors(self):
        response = self.client.get(self.list_authors_url, format='json')
        utils.print_response_info(response, test_name='List Authors Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_selecting_author(self):
        data = {'author_id': self.test_author.id}
        response = self.client.post(self.select_author_url, data, format='json')
        utils.print_response_info(response, test_name='Select Author Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ListSelectBlogPosts(APITestCase):
    def setUp(self):
        self.list_blog_posts_url = '/blog/list-blog-posts/'
        self.select_blog_post_url = '/blog/select-blog-post/'
        self.test_author = Author.objects.create(first_name='John', last_name='Snow')
        self.test_blog_post = BlogPost.objects.create(
                title='A Tale of Two Houses',
                body='John Snow rambling into the night.',
                author=self.test_author
        )

    def test_listing_blog_posts(self):
        response = self.client.get(self.list_blog_posts_url, format='json')
        utils.print_response_info(response, test_name='List Blog Posts Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_selecting_blog_post(self):
        data = {'blog_post_id': self.test_blog_post.id}
        response = self.client.post(self.select_blog_post_url, data, format='json')
        utils.print_response_info(response, test_name='Select Blog Post Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

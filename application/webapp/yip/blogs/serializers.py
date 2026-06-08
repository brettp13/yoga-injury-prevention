from rest_framework import serializers

from .models import Author, BlogPost


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        """
        Manually increment instance id
        """
        instance = self.Meta.model(**validated_data)
        instance.id = Author.objects.latest('id').id + 1
        instance.save()
        return instance

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')
    author_name = serializers.ReadOnlyField(source='author.author_name')

    class Meta:
        model = BlogPost
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        """
        Manually increment instance id
        """
        instance = self.Meta.model(**validated_data)
        instance.id = BlogPost.objects.latest('id').id + 1
        instance.save()
        return instance


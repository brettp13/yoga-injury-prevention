from rest_framework import serializers

from .models import UserProfile, YogaStyle, SearchEntry


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serialize and deserialize user profiles
    """
    user = serializers.ReadOnlyField(source="user.username")
    yoga_style = serializers.ReadOnlyField(source="yoga_style.title")

    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        instance = self.Meta.model(**validated_data)
        instance.id = UserProfile.objects.latest('id').id + 1
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.country = validated_data.get('country', instance.country)
        instance.region = validated_data.get('region', instance.region)
        instance.street = validated_data.get('street', instance.street)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.is_teacher = validated_data.get('is_teacher', instance.is_teacher)
        instance.yoga_style = validated_data.get('yoga_style', instance.yoga_style)
        instance.save()
        return instance


class YogaStyleSerializer(serializers.ModelSerializer):
    """
    Serialize and deserialize yoga styles
    """
    class Meta:
        model = YogaStyle
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.public = validated_data.get('public', instance.public)
        instance.save()


class SearchEntrySerializer(serializers.ModelSerializer):
    """
    Serialize and deserialize search entries
    """
    profile = serializers.ReadOnlyField(source="profile.user")

    class Meta:
        model = SearchEntry
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

